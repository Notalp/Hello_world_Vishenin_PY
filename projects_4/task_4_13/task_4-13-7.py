N = int(input("Введите N: "))
if N <= 0:
    print("Ошибка. N должно быть > 0")
else:
    sum_val = 0
    i = 1
    while i <= N:
        x = float(input("Введите число: "))
        sum_val = sum_val + x
        i = i + 1
    avg = sum_val / N
    print(avg)