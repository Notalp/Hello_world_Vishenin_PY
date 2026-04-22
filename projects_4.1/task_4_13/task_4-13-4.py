N = int(input("Введите N: "))
if N < 1:
    print("Ошибка. Сумма не определена.")
else:
    S = 0
    i = 1
    while i <= N:
        S = S + i
        i = i + 1
    print(S)