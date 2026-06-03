# Список последовательностей ДНК
sequences = ["ATATACGCGTA", "CTTCGGNGGA"]

# Внешний цикл - перебор последовательностей
for seq in sequences:
    print("\n" + "=" * 40)
    print(f"Последовательность: {seq}")
    print("=" * 40)

    # Внутренний цикл - перебор символов в последовательности
    print("ПОСИМВОЛЬНЫЙ ВЫВОД:")
    for letter in seq:
        print(letter)

    print("-" * 40)

# Завершающее сообщение
print("\n✅ Цикл выполнен")