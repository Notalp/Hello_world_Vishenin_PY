# Запрос значения pH у пользователя
ph_value = float(input("Введите значение pH: "))

# Определение среды по значению pH с помощью if/elif/else
if ph_value < 7.0:
    print(f"pH = {ph_value} -- это кислая среда")
elif ph_value == 7.0:
    print(f"pH = {ph_value} -- это нейтральная среда")
else:
    print(f"pH = {ph_value} -- это щелочная среда")