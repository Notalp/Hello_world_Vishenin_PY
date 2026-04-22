N = int(input("Введите N: "))
if N <= 0:
    print("Ошибка. N должно быть > 0")
else:
    count = 0
    i = 1
    while i <= N:
        x = float(input("Введите число: "))
        if x > 0:
            count = count + 1
        i = i + 1
    print(count)