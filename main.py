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
            input_filename = 'data.csv'
            output_filename = 'processed_data.csv'
            data = DataLoader(input_filename).load()
            data = Preprocessor(data).get_data()
            DataSaver(output_filename, data).save()
            print(f"Успех! Данные из {input_filename} были обработаны и помещены в {output_filename}")
        else:
            print("Ошибка! Не обнаружено действие по данному номеру!")
            continue
