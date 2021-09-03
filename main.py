from Parsing.AvitoParser import AvitoParser


if __name__ == "__main__":
    print("Добро пожаловать в Avito-analytics")
    while True:
        print()
        print("Вам доступны следующие действия:")
        print("0. Выход")
        print("1. Начать парсинг данных")

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
        else:
            print("Ошибка! Не обнаружено действие по данному номеру!")
            continue
