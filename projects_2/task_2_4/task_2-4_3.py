# Запрос данных у пользователя
total_capsules = int(input("Введите общее количество произведенных капсул: "))
pack_capacity = int(input("Введите количество капсул в одной упаковке: "))

# Расчет полных упаковок и остатка
full_packs = total_capsules // pack_capacity
remaining_capsules = total_capsules % pack_capacity

# Вывод отчета
print("\n--- Отчет фасовочного цеха ---")
print(f"Полных упаковок: {full_packs}")
print(f"Остаток капсул: {remaining_capsules}")