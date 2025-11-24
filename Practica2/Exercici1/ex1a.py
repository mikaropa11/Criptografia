def maxim_comu_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a

a = int(input("Introdueix un numero: "))
b = int(input("Introdueix un altre numero: "))

mcd = maxim_comu_divisor(a,b)
print(f"Mcd: {mcd}")