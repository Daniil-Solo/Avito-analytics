# Прогнозирование цен квартир в городе Перми по данным с сайта Avito

## Содержание
1. [Актуальность проекта](#Актуальность-проекта)
2. [Особенности сбора данных](#Особенности-сбора-данных)
3. [Обработка "грязных" данных](#Обработка-грязных-данных)
4. [Генерация новых признаков](#Генерация-новых-признаков)
5. [Подготовка множеств](#Подготовка-множеств)
6. [Лучшая полученная модель](#Лучшая-полученная-модель)
7. [Исследование модели](#Исследование-модели)
8. [Как проверить модель](#Как-проверить-модель)   
9. [Стек технологий](#Стек-технологий)
10. [Что можно было улучшить](#Стек-технологий)

---
## Актуальность-проекта
В настоящее время люди достаточно часто продают и покупают квартиры, но адекватно оценить стоимость квартиры довольно проблематично без привлечения служб оценки жилья. 
Данный проект включает в себя построение модели для оценки стоимости недвижимости в городе Перми с учетом характеристик квартиры и дома. 

Так же в отличие от уже существующих работ с похожей тематикой были внедрены признаки окружения: количество образовательных учреждений, учреждений здоровья, заведений культуры, заведений общепита, а так же расстояние до центра города Пермь (городская Эспланада), широта и долгота. 

[:arrow_up:Оглавление](#Содержание)
---

## Особенности сбора данных
Для сбора данных о квартирах был разработан парсер сайта Avito на языке Python с использованием библиотек requests и BeautifulSoup. Работа по извлечению данных усложнялась тем, что различные объявления отличались по своей структуре и иногда приходилось использовать регулярные выражения для получения сведений.

Дополнительная сложность, которая возникла после написания парсера, была связана с тем, что сервер сайта ограничивал количество запросов в единицу времени, а при превышении лимита мог заблокировать по ip на сутки. Для решения данной проблемы в код были добавлены задержки между запросами, что позволило спокойно извлечь все необходимые данные.

По итогам 10-часового парсинга удалось собрать данные о свыше 5500 квартир из города Перми. Собранные признаки: адрес, количество комнат, площадь, количество этажей и этаж квартиры, тип ремонта, тип ванной, вид из окна, тип балкона, год постройки, число лифтов, тип дома, дополнительные услуги. 

[Директория с исходными файлами](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing)

[:arrow_up:Оглавление](#Содержание)
---

## Обработка "грязных" данных
Для подготовки датасета использовалась библиотека pandas, которая позволяет удобно работать с таблицами средствами языка Python. Процесс предобработки состоял из нескольких этапов:
1. Очистка данных:
    * Удаление записей с пропусками важных признаков
    * Выделение признака района из адреса
    * Удаление мусора из данных признаков: количество комнат, площадь, число этажей, тип дома
    * Преобразование года постройки к виду YYYY
    * Заполнение пропусков признака число лифтов, исходя из этажности дома
    * Выделение признаков наличия консьержа, наличия мусоропровода из признака дополнительные услуги
    * Удаление из данных промежуточных признаков 
    * [Скрипт очистки данных](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Preparing_data/1_Data_cleaning.ipynb)
       
2. Работа с выбросами:
    * Исправление некорректного года постройки
    * Было принято решение не удалять выбросы по ценам и площадям, а убрать неадекватные значения с помощью нейронной сети
    * [Скрипт работы с выбросами](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Preparing_data/2_Outliers.ipynb)
       
3. Работа с категориальными признаками:
    * Применения метода one hot кодирования к признакам тип ремонта, тип санузла, тип балкона, тип дома, район
    * [Скрипт работы с категориальными признаками](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Preparing_data/3_Categorical_features.ipynb)
    
[Директория с исходными файлами](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Perparing_data)

[:arrow_up:Оглавление](#Содержание)
---

## Генерация новых признаков
Декодирование адреса квартиры в координаты осуществлялось с помощью сайта [geotree](https://geotree.ru). Для этого был написан скрипт с помощью библиотеки Selenium, который имитировал действия пользователя: автоматически заполнял поле ввода адреса, собирал данные из формы для ответа и вычленял оттуда координаты. [Скрипт получения координат](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Preparing_data/4_Coordinates_generation.ipynb)


Для сбора данных о числе объектов вблизи квартиры использовался [api свободных карт](http://overpass-api.de), для которого был написан скрипт, обращавшийся к сайту с определенной подкатегорий услуг и возвращавший координаты объектов, относящихся к данной подкатегории. 


Всего было выделено 4 категории: 
* __еда__ (кафе, рестораны, фаст-фуд, паб), 
* __здоровье__ (больницы, клиники), 
* __культура__ (кинотеатры, фонтаны, театры), 
* __образование__ (колледжи, университеты, детские сады, школы, библиотеки) 
   
Стоит заметить, что официальный сайт OpenStreetMap является некоммерческим, но открытым для редакции, поэтому на карте города Пермь присутствуют не все объекты, которые есть в настоящее время. 

Для получения информации о том, сколько объектов находится вблизи квартиры использовался алгоритм перевода координат между объектами в расстояние. По такому же принципу был сгенерирован признак дистанции до центра города (Площадь Эспланады).

[Скрипт генерации признаков](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Preparing_data/5_Amenity_feature_generation.ipynb)

[:arrow_up:Оглавление](#Содержание)
---

## Подготовка множеств
Перед формированием множеств была обучена нейронная сеть, состоящая из одного слоя с линейной функцией активации. Это полезная практика, поскольку позволяет выявить неадекватные примеры, которые в будущем будут только мешать обучению.

После удаления неадекватных примеров данные были разбиты на 3 выборки: обучающую (80%), валидационную (10%) и тестовую (10%).

[Скрипт генерации признаков](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Modelling/1_Removing_bad_examples.ipynb)

[:arrow_up:Оглавление](#Содержание)
---

## Лучшая полученная модель
Архитектура модели: 
* Входной слой из 37 нейронов,
* Скрытый слой из 8 нейронов, 
* Выходной слой из 1 нейрона

Между входным и скрытым слоями была использована функция активации под названием ReLU, которая возвращает 0, если поданное значение отрицательное, иначе возвращает само это значение.  

Обновление весов происходило по пакетам для скорейшей сходимости. По этой же причине использовался слой нормализации пакета перед входным слоем.

Для оценки качества модели использовались характеристика коэффициент детерминации R^2, описывающий долю дисперсии реальной цены, объясняемую нейронной сетью. Чем ближе этот коэффициент к единице, тем точнее предсказывает модель. Для тестового множества коэффициент детерминации равен 0.943. Это значит, что модель описывает 94,3 % дисерсии данных. На тренировочном множестве данный показатель равнялся 0.94.

Также для оценки качества использовалась среднеквадратичная относительная погрешность. Для тестового множества данная величина равна 4.56%. Это значит, что в среднем на тестовом множестве модель ошибается на 4,56%. На тренировочном множестве данный показатель равняется 3.15%, что может означать наличие в тестовых данных неадекватных примеров. После просмотра данных оказалось, что тестовая выборка действительно содержала квартиру с очень завышенной ценой.

После построения столбчатых диаграмм с фактической и предсказанной ценой, можно достаточно уверенно говорит, что модель обобщила примеры и вывела общий закон формирования цены на квартиру по имеющимся признакам.

Что касается значимости признаков, то в топ 4 самых значимых признаков вошли 3 инфраструктурных и географических признака, однако наиболее значимым из среди данного набора свойств является площадь квартиры. Для подсчета значимости был написан алгоритм заменяющий значение признака на его медианную величину по выборке и затем считалось изменение ошибки.

[Скрипт обучения и оценки качества лучшей модели](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Modelling/2_Вest_model.ipynb)

[:arrow_up:Оглавление](#Содержание)
---

## Исследование модели
Значимость показывает, что на стоимость квартиры оказывают влияние инфраструктурные и географические признаки. 

Для исследования были выбраны 5 квартир, находящихся вблизи центра города и отличавшиеся по своим внутренним признакам.
Экспериментальная часть заключалась в удалении квартир от центра в определенном направлении. Технически это было реализовано увеличением или уменьшением одной из координат. Таким образом была получена зависимость цены при удалении квартиры на юг, север, запад или восток от центра.

Сложность эксперимента заключалась в том, что при изменении координат необходимо было также изменять значения тех параметров, которые зависели от географического положения, а именно район, количество заведений разных услуг и расстояние до центра.

Для реализации исследования были написаны алгоритмы пересчета расстояний, количества объектов разных услуг и переопределение района посредством обращения к сайту [geotree](https://geotree.ru). 

[Скрипт проведения исследования](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Modelling/3_Research.ipynb)

[:arrow_up:Оглавление](#Содержание)
---

## Как проверить модель
Для того, чтобы получить прогноз от модели необходимо

[:arrow_up:Оглавление](#Содержание)
---
## Стек технологий
* ```Python 3.8```
* ```requests``` ```bs4```  ```lxml``` ```selenium```
* ```pandas``` ```numpy``` ```matplotlib``` ```sklearn```
* ```pytorch```

Версии использованных библиотек приведены в файле [requirements.txt](https://github.com/Daniil-Solo/Avito-analytics/tree/main/requirements.txt)

[:arrow_up:Оглавление](#Содержание)
---

## Что можно было улучшить
1. Сразу с Авито брать данные о координатах домов
2. Найти способ использования коммерческих (более полных) карт для извлечения координат объектов инфраструктуры
3. Использовать вместо калькулятора перевода координат в расстояние что-то более серьезное, например, длину маршрута между объектами на коммерческой карте
ссылка на данные