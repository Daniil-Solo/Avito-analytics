# Прогнозирование цен квартир в городе Перми по данным с сайта Avito
## Задачи на проект
* [Спарсить данные о квартирах в городе Пермь](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing)
* [Провести обработку полученных данных](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Preparing_data)
* [Построить модель для прогноза цены на квартиру по имеющимся характеристикам](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Modelling)

## Стек технологий
* ```Python 3.8```
* ```requests``` ```bs4```  ```lxml``` ```selenium```
* ```pandas``` ```numpy``` ```matplotlib``` ```sklearn```
* ```pytorch```

Версии использованных библиотек приведены в файле [requirements.txt](https://github.com/Daniil-Solo/Avito-analytics/tree/main/requirements.txt)

---
## Актуальность проекта
В настоящее время люди достаточно часто продают и покупают квартиры, но адекватно оценить стоимость квартиры довольно проблематично без привлечения служб оценки жилья. 
Данный проект включает в себя построение модели для оценки стоимости недвижимости в городе Перми с учетом характеристик квартиры и дома. 

Так же в отличие от уже существующих работ с похожей тематикой были внедрены признаки окружения: количество образовательных учреждений, учреждений здоровья, заведений культуры, заведений общепита, а так же расстояние до центра города Пермь (городская Эспланада), широта и долгота. 

---

## Особенности сбора данных
Для сбора данных о квартирах был разработан парсер сайта Avito на языке Python с использованием библиотек requests и BeautifulSoup. Работа по извлечению данных усложнялась тем, что различные объявления отличались по своей структуре и иногда приходилось использовать регулярные выражения для получения сведений.

Дополнительная сложность, которая возникла после написания парсера, была связана с тем, что сервер сайта ограничивал количество запросов в единицу времени, а при превышении лимита мог заблокировать по ip на сутки. Для решения данной проблемы в код были добавлены задержки между запросами, что позволило спокойно извлечь все необходимые данные.

По итогам 10-часового парсинга удалось собрать данные о свыше 5500 квартир из города Перми. Собранные признаки: адрес, количество комнат, площадь, количество этажей и этаж квартиры, тип ремонта, тип ванной, вид из окна, тип балкона, год постройки, число лифтов, тип дома, дополнительные услуги. 

[Директория с исходными файлами](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing)

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

---




---
## Что можно было улучшить
1. Сразу с Авито брать данные о координатах домов
2. Найти способ использования коммерческих (более полных) карт для извлечения координат объектов инфраструктуры
3. Использовать вместо калькулятора перевода координат в расстояние что-то более серьезное, например, длину маршрута между объектами на коммерческой карте
