# Запрос групп крови у пользователя
donor_blood = input("Введите группу крови донора (0, A, B, AB): ").upper()
recipient_blood = input("Введите группу крови реципиента (0, A, B, AB): ").upper()

# Проверка возможности переливания крови
if donor_blood == recipient_blood:
    print(f"✅ Переливание возможно: группа {donor_blood} совместима с группой {recipient_blood}")
elif donor_blood == "0":
    print(f"✅ Переливание возможно: группа 0 (универсальный донор) подходит для группы {recipient_blood}")
else:
    print(f"❌ Переливание НЕВОЗМОЖНО: группа {donor_blood} не подходит для группы {recipient_blood}")