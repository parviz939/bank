import json
from copy import deepcopy

# сохраняй данный json
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

#Данная c json считай
def load_data():
    with open("data.json") as f:
        data = json.load(f)

    return data

#Принимает имя валюты и её % и показывает пропорционально сколько это валюта займа Нашем Портфели
def show_percent(name, percent, width = 50):
    fill = "|"
    empty = "-"
    bars = round(percent * width)

    progress = fill * bars + empty * (width - bars)
    print(f"{name:10} + {round(percent * 100)}% |{progress}|")

#Принимает два списка 1 столбики которые мы хотим нарисовать а второй подписок и столбам
def plot_stat(data, signs, height = 12):

    for i in range(height):
        if i % 3 ==0 :
            current = max(data) - (max(data) - min(data)) / height * i
            line = f"{str(round(current, 1)):10}"
        else:
            line = " "*10
        for num in data:
            if max(data) - (max(data)-min(data))/height*(i+1) < num:
                    line += "|   "
        else:
                line += "     "

        print(line)
    print(f"{str(round(min(data), 1)):10}" + "|   " * len(data))
    print(" "*10 + "|   " * len(data))
    line = (" "*10)
    for sign in signs:
        line += f"{sign:4}"

    print(line)

#Переводит все валюты всей недели в доллары и потом строить график
def show_convert(data):
    weeks = list(sorted(data.keys()))
    converted = []

    for week in weeks:
        currencies = data[week]
        total = 0
        for curr in  currencies:
            total += curr["cost"] * curr["amount"]

        converted.append(round(total, 2))
    plot_stat(converted, weeks)

#Подсчитывает для какой-то недели В долларах то сколько валюта занимает место в нашем  портфеле
def show_stat(data, weeknum):
    total = 0
    for curr in data[weeknum]:
        total += curr["cost"] * curr["amount"]

    stats = []
    for curr in data[weeknum]:
        stats.append( ( curr["cost"] * curr["amount"] / total, curr["name"]) )

        stats = reversed(sorted(stats))

        for s, name in stats:
            show_percent(name, s)
#Показывает какие режимы
def select_mode():
    print()
    print ("_"*30)
    print(" Выберите режим работы:")
    print("1. Добавить новую неделю")
    print("2. Скопировать новую неделю")
    print("3. Добавить информацию о валюте")
    print("4. Изменить информацию о валюте")
    print("5. Вывести статистику")
    print("6. Вывести распределение валют")
    print("7. Выйти из программы")
    print("-"*30)
    print()
    return int(input())

#Бесконечный цикл Каждый режим обрабатываю по-своему
def loop():
    data = load_data()

    while True:
        mode = select_mode()

        if mode == 1:
            name = input("Введите номер недели: ")
            data[name] = []
        elif mode == 2:
            week = input("Введите номер  недели: ")
            from_week = input("Введите номер неделе откуда будем копировать: ")

            data[week] = deepcopy(data[from_week])
        elif mode == 3:
            week = input(" Введите номер недели: ")
            name = input(" Введите имя валюты: ")
            cost = float(input(" Введите стоимость валюты: "))
            amount = float(input(" Введите количество валюты: "))

            data[week].append({
                "name": name,
                "cost": cost,
                "amount": amount
            })
        elif mode == 4:
            week = input(" Введите номер недели: ")
            name = input(" Введите имя валюты: ")

            num = None
            for i, curr in enumerate(data[week]):
                if curr["name"] == name:
                    num = i

            if num == None:
                print("Нет такой валюты!")
            else:
                curr_cost = data[name][num]["cost"]
                cost = input(f" Введите стоимость валюты ({curr_cost}): ")
                if cost:
                    data[name][num]["cost"] = float(cost)

                corr_amount = data[week][num]["amount"]
                amount = input(f" Видите коллектива валюты ({corr_amount}) ")
                if amount:
                    data[week][num]["amount"] =float(amount)


        elif mode == 5:
            show_convert(data)
        elif mode == 6:
            week = input(" Введите номер недели: ")
            #show_sata(data, week)
        elif mode == 7:
            break
        else:
            print("Некорректный режим!")

#Сохранить данные
    save_data(data)

loop()
#            week = input("Введите номер новой недели: ")
#            from_week = input(
#                " Введите номер недели, откуда будем копировать: ")
#            data[week] = deepcopy(data[from_week])


#plot_stat([3, 5, 1, 4], ["A", "B", "C", "P"] )

