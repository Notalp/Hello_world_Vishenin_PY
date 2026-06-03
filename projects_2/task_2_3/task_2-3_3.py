# Сбор данных от пользователя
researcher_name = input("Введите ФИО исследователя: ")
date = input("Введите дату (ДД.ММ.ГГГГ): ")
experiment_name = input("Введите название эксперимента: ")
experiment_conclusion = input("Введите вывод по эксперименту: ")

# Создание файла с красивой рамкой
with open("journal.txt", "w", encoding="utf-8") as file:
    # Верхняя граница
    file.write("+---+\n")
    file.write("| Электронный лабораторный журнал |\n")
    file.write("+---+\n")

    # Основная информация
    file.write(f"| ФИО исследователя : {researcher_name} |\n")
    file.write(f"| Дата : {date} |\n")
    file.write(f"| Эксперимент : {experiment_name} |\n")

    # Разделитель
    file.write("+---+\n")

    # Вывод (может быть многострочным)
    file.write("| Вывод: |\n")

    # Разбиваем вывод на строки по 40 символов для красивой рамки
    words = experiment_conclusion.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= 40:
            if line:
                line += " " + word
            else:
                line = word
        else:
            file.write(f"| {line.ljust(40)} |\n")
            line = word
    if line:
        file.write(f"| {line.ljust(40)} |\n")

    # Нижняя граница
    file.write("+---+\n")

print("Данные успешно сохранены в journal.txt")