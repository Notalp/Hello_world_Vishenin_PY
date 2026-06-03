N = int(input("Введите N: "))
if N <= 0:
    print("Ошибка. N должно быть > 0")
else:
    sum_val = 0
    count = 0
    i = 1
    while i <= N:
        x = float(input("введите число: "))
        if (i - 1) % 2 == 0: #или i % 2 == 0 ????
            sum_val += x
            count += 1
        i += 1
    if count > 0:
        avg = sum_val / count
        print(avg)