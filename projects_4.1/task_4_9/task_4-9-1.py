x = float(input("Введите число X: "))
y = float(input("Введите число Y: "))
if x > y:
    max_value = x
else:
    max_value = y
print(f"Максимальное число: {max_value: .0f}")