import sys
import os

# Afegeix el path absolut de la carpeta 'Exercici1' al path de Python
ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_exercici1 = os.path.join(ruta_base, 'Exercici1')
sys.path.append(ruta_exercici1)

from ex1b import euclides_extes, invers_modular
from ex1c import exponenciacio_binaria



def rsa_interactiu():
    print("---- RSA PAS A PAS ----\n")

    # i) Demanem dos nombres primers
    p = int(input("Introdueix un nombre primer p: "))
    q = int(input("Introdueix un altre nombre primer q: "))
    print(f"1) Nombres primers: p = {p}, q = {q}")

    # ii) Calculem el mòdul n
    n = p * q
    print(f"2) Calculem n = p · q = {n}")

    # iii) Calculem φ(n)
    phi_n = (p - 1) * (q - 1)
    print(f"3) Funció d’Euler φ(n) = (p-1)(q-1) = {phi_n}")

    # iv) Triem un exponent públic e vàlid (petit i coprimer amb φ(n))
    e = int(input(f"Introdueix un exponent públic e (1 < e < {phi_n}, coprimer amb {phi_n}): "))
    gcd, _, _ = euclides_extes(e, phi_n)
    if gcd != 1:
        print(f"Error: {e} no és coprimer amb {phi_n}. Torna-ho a provar.")
        return

    print(f"4) Exponent públic: e = {e}, amb gcd(e, φ(n)) = {gcd}")

    # v) Calculem l'invers modular d
    d = invers_modular(e, phi_n)
    print(f"5) Invers modular de {e} mod {phi_n} → d = {d}")

    # vi) Claus pública i privada
    print(f"6) Clau pública: (n, e) = ({n}, {e})")
    print(f"   Clau privada: (n, d) = ({n}, {d})")

    # vii) Xifrar un missatge
    m = int(input(f"\nIntrodueix el missatge a xifrar (m < {n}): "))
    c = exponenciacio_binaria(m, e, n)
    print(f"7) Missatge xifrat: c = m^e mod n = {m}^{e} mod {n} = {c}")

    # viii) Desxifrar el missatge
    m_desencriptat = exponenciacio_binaria(c, d, n)
    print(f"8) Missatge desxifrat: m = c^d mod n = {c}^{d} mod {n} = {m_desencriptat}")

    # Verificació
    if m_desencriptat == m:
        print("\nMissatge desxifrat correctament! Hem recuperat l'original.")
    else:
        print("\nError: el missatge desxifrat no coincideix amb l'original.")

# Cridar la funció principal
rsa_interactiu()
