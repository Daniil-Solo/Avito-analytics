from Parsing.AvitoParser import AvitoParser
from ETL.preprocessing import Preprocessor, DataLoader, DataSaver


if __name__ == "__main__":
    print("Добро пожаловать в Avito-analytics")
    while True:
        print()
        print("Вам доступны следующие действия:")
        print("0. Выход")
        print("1. Начать парсинг данных")
        print("2. Предобработать данные")

        answer = input("Ваш ответ: ")
        try:
            choice = int(answer)
        except ValueError:
            print("Ошибка! Вам следует указать номер действия!")
            continue

        if choice == 0:
            exit(1)
        elif choice == 1:
            parser = AvitoParser()
            parser.start()
        elif choice == 2:
            data = DataLoader('data.csv').load()
            data = Preprocessor(data).get_data()
            DataSaver('new_data.csv', data).save()
        else:
            print("Ошибка! Не обнаружено действие по данному номеру!")
            continue
