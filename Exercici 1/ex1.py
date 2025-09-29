def analizar_frecuencia(texto):
    frecuencia = {}
    for char in texto:
        if char.isalpha():
            if char in frecuencia:
                frecuencia[char] += 1
            else:
                frecuencia[char] = 1
    return frecuencia

def descifrar_cesar(texto):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    texto = texto.upper()
    
    for desplazamiento in range(1, len(alfabeto)):
        descifrado = ""
        for char in texto:
            if char in alfabeto:
                indice = alfabeto.index(char)
                nuevo_indice = (indice - desplazamiento) % len(alfabeto)
                descifrado += alfabeto[nuevo_indice]
            else:
                descifrado += char
        print(f"Desplazamiento {desplazamiento}: {descifrado}")


texto_cifrado = "T SLGP DPPY ESTYRD JZF APZAWP HZFWO YZE MPWTPGP, LEELNV DSTADZY QTCP ZQQ ESP DSZFWOPC ZQ ZCTZY, T HLENSPO N-MPLXD RWTEEPCTY ESP OLCV YPLC ESP ELYYSLFDPC RLEP. LWW ESZDP XZXPYED HTWWMP WZDE TY ETXP, WTVP EPLCD TY CLTY. ETXP EZ OTP."

print("Análisis de frecuencia del texto cifrado:")
print(analizar_frecuencia(texto_cifrado))
descifrar_cesar(texto_cifrado)