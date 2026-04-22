N = int(input("Введите N: "))
if N < 0:
    print("Ошибка. N должно быть >= 0")
else:
    S = 0
    i = 1
    while i <= N:
        S = S + i ** 2
        i = i + 1
    print(S)