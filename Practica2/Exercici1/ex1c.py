def exponenciacio_binaria(m, e, n):
    resultat = 1
    m = m % n  # Ens assegurem que m < n per evitar nombres grans innecessaris

    while e > 0:
        if e % 2 == 1:         # Si el bit actual d'e és 1
            resultat = (resultat * m) % n
        m = (m * m) % n        # Quadrat del base
        e = e // 2             # Anem al següent bit (divisió per 2)
    
    return resultat

# m = int(input("Introdueix el valor de m: "))
# e = int(input("Introdueix el valor de e: "))
# n = int(input("Introdueix el valor de n: "))

# res = exponenciacio_binaria(m, e, n)
# print(f"{m}^{e} mod {n} = {res}")