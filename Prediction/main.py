import tkinter as tk
from tkinter import ttk
from functions import get_price


def create_window():
    def calculate():
        try:
            data = [float(ent_n_rooms.get()), float(ent_area.get()), float(ent_n_floors.get()), float(ent_floor.get()),
                    float(ent_year.get()), float(ent_lift.get()), float(cmb_conc.current()), float(cmb_garbage.current())]
            repair_list = [0] * 4
            repair_list[cmb_repair.current()] = 1
            data += repair_list
            bath_list = [0] * 3
            bath_list[cmb_bath.current()] = 1
            data += bath_list
            terrace_list = [0] * 3
            terrace_list[cmb_terrace.current()] = 1
            data += terrace_list
            house_type_list = [0] * 5
            house_type_list[cmb_house_type.current()] = 1
            data += house_type_list
            district_list = [0] * 7
            district_list[cmb_district.current()] = 1
            data += district_list
            data.append(float(ent_lat.get()))
            data.append(float(ent_lon.get()))
            result = get_price(data)

            lbl_result['text'] = "Стоимость: " + str(round(result/1000_000, 3)) + " млн."
        except ValueError:
            pass

    root = tk.Tk()
    root.title("Предсказание стоимости квартиры")
    root.geometry("380x420")
    frame = tk.Frame(root)
    frame.pack()

    lbl_n_rooms = tk.Label(frame, text="Количество комнат")
    ent_n_rooms = tk.Entry(frame, width=20)
    lbl_n_rooms.grid(row=1, column=0)
    ent_n_rooms.grid(row=1, column=1, sticky="e")

    lbl_area = tk.Label(frame, text="Площадь")
    ent_area = tk.Entry(frame, width=20)
    lbl_area.grid(row=2, column=0)
    ent_area.grid(row=2, column=1, sticky="e")

    lbl_n_floors = tk.Label(frame, text="Количество этажей в доме")
    ent_n_floors = tk.Entry(frame, width=20)
    lbl_n_floors.grid(row=3, column=0)
    ent_n_floors.grid(row=3, column=1, sticky="e")

    lbl_floor = tk.Label(frame, text="Этаж квартиры")
    ent_floor = tk.Entry(frame, width=20)
    lbl_floor.grid(row=4, column=0)
    ent_floor.grid(row=4, column=1, sticky="e")

    lbl_year = tk.Label(frame, text="Год постройки")
    ent_year = tk.Entry(frame, width=20)
    lbl_year.grid(row=5, column=0)
    ent_year.grid(row=5, column=1, sticky="e")

    lbl_lift = tk.Label(frame, text="Количество лифтов")
    ent_lift = tk.Entry(frame, width=20)
    lbl_lift.grid(row=6, column=0)
    ent_lift.grid(row=6, column=1, sticky="e")

    lbl_conc = tk.Label(frame, text="Консьерж")
    cmb_conc = ttk.Combobox(frame, values=["Нет", "Есть"], width=16)
    cmb_conc.set("Выберите ответ")
    lbl_conc.grid(row=7, column=0)
    cmb_conc.grid(row=7, column=1, sticky="e", padx=5, pady=5)

    lbl_garbage = tk.Label(frame, text="Мусоропровод")
    cmb_garbage = ttk.Combobox(frame, values=["Нет", "Есть"], width=16)
    cmb_garbage.set("Выберите ответ")
    lbl_garbage.grid(row=8, column=0)
    cmb_garbage.grid(row=8, column=1, sticky="e", padx=5, pady=5)

    lbl_repair = tk.Label(frame, text="Ремонт")
    cmb_repair = ttk.Combobox(frame, values=["Дизайнерский", "Евро", "Косметический", "Требует ремонта"], width=16)
    cmb_repair.set("Выберите ответ")
    lbl_repair.grid(row=9, column=0)
    cmb_repair.grid(row=9, column=1, sticky="e", padx=5, pady=5)

    lbl_bath = tk.Label(frame, text="Санузел")
    cmb_bath = ttk.Combobox(frame, values=["Несколько", "Раздельный", "Совмещенный"], width=16)
    cmb_bath.set("Выберите ответ")
    lbl_bath.grid(row=10, column=0)
    cmb_bath.grid(row=10, column=1, sticky="e", padx=5, pady=5)

    lbl_terrace = tk.Label(frame, text="Балкон")
    cmb_terrace = ttk.Combobox(frame, values=["Балкон", "Лоджия", "Нет"], width=16)
    cmb_terrace.set("Выберите ответ")
    lbl_terrace.grid(row=11, column=0)
    cmb_terrace.grid(row=11, column=1, sticky="e", padx=5, pady=5)

    lbl_house_type = tk.Label(frame, text="Тип дома")
    cmb_house_type = ttk.Combobox(frame, values=["Блочный", "Деревянный", "Кирпичный", "Монолитный", "Панельный"],
                                  width=16)
    cmb_house_type.set("Выберите ответ")
    lbl_house_type.grid(row=12, column=0)
    cmb_house_type.grid(row=12, column=1, sticky="e", padx=5, pady=5)

    lbl_district = tk.Label(frame, text="Район")
    cmb_district = ttk.Combobox(frame, values=["Дзержинский", "Индустриальный", "Кировский", "Ленинский",
                                               "Мотовилихинский", "Орджоникидзевский", "Свердловский"],
                                width=16)
    cmb_district.set("Выберите ответ")
    lbl_district.grid(row=13, column=0)
    cmb_district.grid(row=13, column=1, sticky="e", padx=5, pady=5)

    lbl_lat = tk.Label(frame, text="Широта")
    ent_lat = tk.Entry(frame, width=20)
    lbl_lat.grid(row=14, column=0)
    ent_lat.grid(row=14, column=1, sticky="e")

    lbl_lon = tk.Label(frame, text="Долгота")
    ent_lon = tk.Entry(frame, width=20)
    lbl_lon.grid(row=15, column=0)
    ent_lon.grid(row=15, column=1, sticky="e")

    button = tk.Button(frame, text="Рассчитать стоимость", command=calculate)
    button.grid(row=16, column=0, padx=5, pady=5)
    lbl_result = tk.Label(frame, text="Стоимость: ")
    lbl_result.grid(row=16, column=1)

    root.mainloop()


if __name__ == "__main__":
    create_window()
