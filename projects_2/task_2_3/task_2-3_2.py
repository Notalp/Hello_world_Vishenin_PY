# Запрос данных у пользователя
operator_name = input("Введите имя оператора: ")
pressure_value = input("Введите текущее значение давления (Па): ")

# Сохранение данных в файл sensor_log.txt в формате таблицы
with open("sensor_log.txt", "a", encoding="utf-8") as file:
    file.write(f"{operator_name}\t{pressure_value}\n")

# Вывод сообщения об успехе
print("Данные успешно сохранены в sensor_log.txt")