# Директория парсинга
## Описание файлов
Данная директория содержит следующие файлы:
1. [AvitoParser.py](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing/AvitoParser.py) - класс парсера
2. [Handler.py](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing/Handler.py) - классы для обработчиков полей
3. [Page.py](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing/Page.py) - класс обработки страницы списка квартир
4. [Post.py](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing/Post.py) - класс обработки страницы объявления
5. [config.json](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing/configs.json) - файл с настройками для парсера
6. [main.py](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing/main.py) - код для запуска парсера

## Подготовка к парсингу
В файле [config.json](https://github.com/Daniil-Solo/Avito-analytics/tree/main/Parsing/configs.json) можно задать:
1. Ссылку на первую страницу с квартирами
2. Название выходного файла с расширением csv
3. Поля, информация о которых будет занесена в таблицу

## Запуск парсера
Программа запускается следующей строчкой на консоли в папке проекта:
```
>>> python3 main.py
```

## Извлекаемые данные
- физический адрес
- количество комнат
- площадь квартиры
- количество этажей в доме
- этаж квартиры
- цена
- ссылка на объявление
- текст объявления
- ремонт
- санузел
- вид из окон
- год постройки
- лифт
- дополнительные услуги
- тип дома
- парковка