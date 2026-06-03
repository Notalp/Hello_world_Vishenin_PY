reactant_name = input("Введите название реактива: ")
reactant_quantity = int(input("Введите количество (целое число): "))

report = f"Реактив {reactant_name} поступил на склад в количестве {reactant_quantity} шт."

print(report)

with open("inventory.txt", "w", encoding="utf-8") as file:
    file.write(report)

print("Отчет также сохранен в файл inventory.txt")