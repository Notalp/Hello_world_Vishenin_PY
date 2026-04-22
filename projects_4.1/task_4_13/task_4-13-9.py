N = int(input("Введите N: "))
if N <= 0:
    print("Ошибка. N должно быть > 0")
else:
    sum_val = 0
    i = 1
    while i <= N:
        x = int(input("Введите число: "))
        if i % 2 != 0:
            sum_val += x
        i += 1
    print(sum_val)