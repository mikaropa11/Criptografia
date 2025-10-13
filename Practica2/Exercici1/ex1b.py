def euclides_extes(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x1, y1 = euclides_extes(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return d, x, y

def invers_modular(d, n):
    d = d % n  # Ens assegurem que d està dins del mòdul
    gcd, x, _ = euclides_extes(d, n)
    if gcd != 1:
        return None  # No hi ha invers si no són coprimers
    return x % n  # L'invers ha de ser dins de Z_n

def son_coprimers_i_invers(d, n):
    invers = invers_modular(d, n)
    if invers is None:
        print(f"{d} i {n} no són coprimers. No existeix invers modular.")
    else:
        print(f"{d} i {n} són coprimers. L'invers de {d} mod {n} és {invers}.")
    return invers

# Exemple d'ús
# d = int(input("Introdueix el valor de d: "))
# n = int(input("Introdueix el valor de n: "))

# son_coprimers_i_invers(d, n)