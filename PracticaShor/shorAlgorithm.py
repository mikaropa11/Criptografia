import numpy as np
import random
from math import gcd, log2, ceil
from fractions import Fraction


class ShorAlgorithm:
    """
    Implementació completa de l'Algorisme de Shor amb simulació
    dels components quàntics.
    """
    
    def __init__(self, N):
        """
        Inicialitza l'algorisme per factoritzar N.
        
        Args:
            N (int): Número a factoritzar
        """
        self.N = N
        self.n_qubits = ceil(2 * log2(N))  # Nombre de qubits necessaris
    
    # ========== FUNCIONS AUXILIARS CLÀSSIQUES ==========
    
    def mod_pow(self, base, exp, mod):
        """
        Calcula (base^exp) mod mod de forma eficient.
        Exponenciació modular ràpida.
        """
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result
    
    def choose_random_a(self):
        """
        Escull un valor aleatori 'a' amb gcd(a, N) = 1.
        """
        while True:
            a = random.randint(2, self.N - 1)
            if gcd(a, self.N) == 1:
                return a
    
    # ========== SIMULACIÓ DEL MÒDUL QUÀNTIC ==========
    
    def create_uniform_quantum_register(self):
        """
        1. Creació d'un registre quàntic uniforme.
        Crea un registre de n qubits en superposició uniforme.
        
        Returns:
            np.array: Vector d'estats amb amplituds uniformes
        """
        size = 2 ** self.n_qubits
        amplitude = 1.0 / np.sqrt(size)
        
        # Cada estat |x⟩ té la mateixa amplitud
        register = np.full(size, amplitude, dtype=complex)
        
        print(f"\n[QUÀNTIC] Registre creat amb {self.n_qubits} qubits ({size} estats)")
        print(f"[QUÀNTIC] Amplitud per estat: {amplitude:.6f}")
        
        return register
    
    def quantum_modular_exponentiation(self, register, a):
        """
        2. Entrellaçament: Exponenciació modular.
        Aplica l'operació |x⟩ → |x, a^x mod N⟩
        
        Args:
            register: Registre quàntic inicial
            a: Base de l'exponenciació
            
        Returns:
            dict: Diccionari que mapeja x → (a^x mod N, amplitud)
        """
        entangled = {}
        
        for x in range(len(register)):
            if abs(register[x]) > 1e-10:  # Ignorar amplituds negligibles
                fx = self.mod_pow(a, x, self.N)
                
                if fx not in entangled:
                    entangled[fx] = []
                entangled[fx].append((x, register[x]))
        
        print(f"[QUÀNTIC] Exponenciació modular aplicada: |x⟩ → |x, {a}^x mod {self.N}⟩")
        print(f"[QUÀNTIC] Estats entrellaçats: {len(entangled)} valors diferents de f(x)")
        
        return entangled
    
    def measure_second_register(self, entangled):
        """
        3. Mesura del segon registre.
        Mesura el segon registre i col·lapsa el primer.
        
        Args:
            entangled: Estats entrellaçats
            
        Returns:
            np.array: Registre col·lapsat després de la mesura
        """
        # Calcular probabilitats per cada valor de f(x)
        probabilities = {}
        for fx, states in entangled.items():
            prob = sum(abs(amp) ** 2 for _, amp in states)
            probabilities[fx] = prob
        
        # Mesurar (col·lapsar) a un valor aleatori segons les probabilitats
        values = list(probabilities.keys())
        probs = list(probabilities.values())
        measured_fx = random.choices(values, weights=probs)[0]
        
        print(f"[QUÀNTIC] Mesura del segon registre: f(x) = {measured_fx}")
        
        # Col·lapsar el primer registre: mantenir només estats amb f(x) = measured_fx
        collapsed_states = entangled[measured_fx]
        
        # Crear nou registre col·lapsat i renormalitzar
        size = 2 ** self.n_qubits
        collapsed_register = np.zeros(size, dtype=complex)
        
        for x, amp in collapsed_states:
            collapsed_register[x] = amp
        
        # Renormalitzar
        norm = np.sqrt(np.sum(np.abs(collapsed_register) ** 2))
        collapsed_register /= norm
        
        print(f"[QUÀNTIC] Registre col·lapsat a {len(collapsed_states)} estats")
        
        return collapsed_register
    
    def quantum_fourier_transform(self, register):
        """
        4. Aplicació de la QFT (Transformada de Fourier Quàntica).
        Utilitza FFT per simular la QFT.
        
        Args:
            register: Registre quàntic
            
        Returns:
            np.array: Registre després d'aplicar QFT
        """
        print(f"[QUÀNTIC] Aplicant Transformada de Fourier Quàntica...")
        
        # La QFT és essencialment una DFT (Discrete Fourier Transform)
        # Podem usar numpy.fft per simular-ho
        qft_register = np.fft.fft(register) / np.sqrt(len(register))
        
        return qft_register
    
    def measure_qft_register(self, qft_register):
        """
        Mesura el registre després de la QFT.
        Retorna l'estat més probable.
        
        Args:
            qft_register: Registre després de QFT
            
        Returns:
            int: Estat mesurat
        """
        probabilities = np.abs(qft_register) ** 2
        measured_state = np.random.choice(len(qft_register), p=probabilities)
        
        print(f"[QUÀNTIC] Estat mesurat després de QFT: {measured_state}")
        
        return measured_state
    
    def continued_fraction_expansion(self, measured_state):
        """
        5. Càlcul del període mitjançant fraccions continues.
        
        Args:
            measured_state: Estat mesurat després de QFT
            
        Returns:
            int: Període candidat r
        """
        M = 2 ** self.n_qubits
        
        # Convertir measured_state / M a fracció usando fraccions continues
        if measured_state == 0:
            return 1
        
        fraction = Fraction(measured_state, M).limit_denominator(self.N)
        
        print(f"[QUÀNTIC] Fracció contínua: {measured_state}/{M} ≈ {fraction}")
        
        r = fraction.denominator
        
        # Verificar que r sigui vàlid
        if r % 2 == 0 and r > 0:
            # Verificar que a^r ≡ 1 (mod N)
            if self.mod_pow(self.current_a, r, self.N) == 1:
                print(f"[QUÀNTIC] Període trobat: r = {r}")
                return r
        
        # Si no és vàlid, provar múltiples del denominador
        for multiplier in range(2, self.N):
            r_candidate = fraction.denominator * multiplier
            if r_candidate >= self.N:
                break
            if r_candidate % 2 == 0:
                if self.mod_pow(self.current_a, r_candidate, self.N) == 1:
                    print(f"[QUÀNTIC] Període trobat (múltiple): r = {r_candidate}")
                    return r_candidate
        
        print(f"[QUÀNTIC] Període candidat (pot no ser òptim): r = {fraction.denominator}")
        return fraction.denominator
    
    def quantum_period_finding(self, a):
        """
        Mòdul quàntic complet: troba el període r de f(x) = a^x mod N.
        
        Args:
            a: Base de l'exponenciació
            
        Returns:
            int: Període r
        """
        self.current_a = a
        print("\n" + "="*60)
        print("INICI DEL MÒDUL QUÀNTIC")
        print("="*60)
        
        # Pas 1: Crear registre quàntic uniforme
        register = self.create_uniform_quantum_register()
        
        # Pas 2: Aplicar exponenciació modular (entrellaçament)
        entangled = self.quantum_modular_exponentiation(register, a)
        
        # Pas 3: Mesurar segon registre
        collapsed_register = self.measure_second_register(entangled)
        
        # Pas 4: Aplicar QFT
        qft_register = self.quantum_fourier_transform(collapsed_register)
        
        # Pas 5: Mesurar i trobar període amb fraccions continues
        measured_state = self.measure_qft_register(qft_register)
        r = self.continued_fraction_expansion(measured_state)
        
        print("="*60)
        print("FI DEL MÒDUL QUÀNTIC")
        print("="*60 + "\n")
        
        return r
    
    # ========== PART CLÀSSICA DE L'ALGORISME ==========
    
    def factorize(self, max_attempts=10):
        """
        Executa l'algorisme de Shor complet.
        
        Args:
            max_attempts: Nombre màxim d'intents
            
        Returns:
            tuple: (p, q) factors de N, o (None, None) si no es troben
        """
        print(f"\n{'='*60}")
        print(f"ALGORISME DE SHOR - Factoritzant N = {self.N}")
        print(f"{'='*60}\n")
        
        # Cas trivial: N parell
        if self.N % 2 == 0:
            print(f"N = {self.N} és parell!")
            return (2, self.N // 2)
        
        # Cas trivial: N és una potència
        for b in range(2, int(self.N ** 0.5) + 1):
            exp = 2
            while b ** exp <= self.N:
                if b ** exp == self.N:
                    print(f"N = {self.N} és una potència: {b}^{exp}")
                    return (b, b ** (exp - 1))
                exp += 1
        
        # Algorisme de Shor principal
        for attempt in range(max_attempts):
            print(f"\n--- INTENT {attempt + 1} ---")
            
            # Escollir 'a' aleatori amb gcd(a, N) = 1
            a = self.choose_random_a()
            print(f"a = {a} escollit aleatòriament")
            
            g = gcd(a, self.N)
            if g != 1:
                print(f"Sort! gcd({a}, {self.N}) = {g} != 1")
                return (g, self.N // g)
            
            print(f"gcd({a}, {self.N}) = 1 ✓")
            
            # Trobar període r usant el mòdul quàntic
            r = self.quantum_period_finding(a)
            
            # Verificar que r sigui parell
            if r % 2 != 0:
                print(f"r = {r} és senar. Tornant a intentar...")
                continue
            
            print(f"r = {r} és parell ✓")
            
            # Verificar que a^(r/2) ≢ -1 (mod N)
            half_power = self.mod_pow(a, r // 2, self.N)
            if half_power == self.N - 1:
                print(f"{a}^{r//2} ≡ -1 (mod {self.N}). Tornant a intentar...")
                continue
            
            print(f"{a}^{r//2} ≡ {half_power} (mod {self.N}) ✓")
            
            # Calcular factors
            p = gcd(self.mod_pow(a, r // 2, self.N) - 1, self.N)
            q = gcd(self.mod_pow(a, r // 2, self.N) + 1, self.N)
            
            print(f"\nCalculant factors:")
            print(f"p = gcd({a}^{r//2} - 1, {self.N}) = {p}")
            print(f"q = gcd({a}^{r//2} + 1, {self.N}) = {q}")
            
            # Verificar que siguin factors vàlids
            if p > 1 and q > 1 and p * q == self.N:
                print(f"\n{'='*60}")
                print(f"✓ FACTORS TROBATS: {p} × {q} = {self.N}")
                print(f"{'='*60}\n")
                return (p, q)
        
        print(f"\nNo s'han trobat factors després de {max_attempts} intents.")
        return (None, None)


# ========== PROGRAMA PRINCIPAL ==========

if __name__ == "__main__":
    print("\n" + "█"*60)
    print(" "*15 + "ALGORISME DE SHOR")
    print("█"*60)
    
    # Demanar N a l'usuari
    while True:
        try:
            N = int(input("\nIntrodueix el número a factoritzar (N >= 4): "))
            if N < 4:
                print("Error: N ha de ser >= 4")
                continue
            if N == 1 or N == 2 or N == 3:
                print(f"N = {N} és trivial (nombre primer o massa petit)")
                continue
            break
        except ValueError:
            print("Error: Introdueix un número enter vàlid")
    
    # Executar l'algorisme de Shor
    shor = ShorAlgorithm(N=N)
    p, q = shor.factorize()
    
    # Mostrar resultats
    if p and q:
        print(f"\n{'█'*60}")
        print(f"  RESULTAT FINAL: {N} = {p} × {q}")
        print(f"{'█'*60}\n")
    else:
        print(f"\n{'█'*60}")
        print(f"  No s'han pogut trobar els factors de {N}")
        print(f"{'█'*60}\n")