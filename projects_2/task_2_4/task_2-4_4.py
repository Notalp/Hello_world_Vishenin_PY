# Запрос нужного объема раствора
volume = float(input("Введите нужный объем физиологического раствора (мл): "))

# Расчет массы соли для 0.9% концентрации
# 0.9% означает 0.9 г соли на 100 мл раствора
salt_mass = volume * 0.009

# Объем воды примерно равен общему объему
water_volume = volume

# Вывод рецепта в файл recipe.txt
with open("recipe.txt", "w", encoding="utf-8") as file:
    file.write("ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n")
    file.write("---\n")
    file.write(f"Общий объем: {volume} мл\n")
    file.write(f"Масса соли: {salt_mass:.2f} г\n")
    file.write(f"Объем воды: {water_volume} мл\n")

# Вывод сообщения об успехе
print("Рецепт сохранен в файл recipe.txt")