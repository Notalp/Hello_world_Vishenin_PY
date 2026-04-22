A = float(input("Введите A: "))
B = float(input("Введите B: "))
C = float(input("Введите C: "))
D = float(input("Введите D: "))
min_val = A
if B < min_val:
    min_val = B
if C < min_val:
    min_val = C
if D < min_val:
    min_val = D
print(f"min = {min_val:.0f}" if min_val.is_integer() else f"min = {min_val}")