import random
def cifrar_cesar(texto, desplazamiento):
    resultado = ""

    for char in texto:
        if char.isalpha():
            desplazamiento_base = ord('A') if char.isupper() else ord('a')
            nuevo_char = chr((ord(char) - desplazamiento_base + desplazamiento) % 26 + desplazamiento_base)
            resultado += nuevo_char
        else:
            resultado += char

    return resultado

def cifrar_homofonos(texto):
    mapa_cifrado = {
        "E": ["3", "F", "J", "9", "Ω", "Σ"],
        "A": ["1", "L", "D", "8", "β"],
        "O": ["7", "Q", "ψ", "4"],
        "S": ["2", "M", "χ", "5"],
        "R": ["Z", "δ", "6"],
        "N": ["G", "ξ", "0"],
        "I": ["V", "μ", "ϕ"],
        "D": ["T", "κ", "2"],
        "L": ["U", "θ", "λ"],
        "T": ["C", "α", "3"],
        "U": ["H", "η", "ν"],
        "C": ["Y", "φ"],
        "M": ["X", "ρ"],
        "P": ["K", "π"],
        "B": ["W"],
        "G": ["N"],
        "V": ["ϖ"],
        "Y": ["Δ"],
        "Q": ["Ψ"],
        "H": ["ζ"],
        "F": ["σ"],
        "Z": ["ω"],
        "J": ["χ"],
        "Ñ": ["γ"],
        "X": ["τ"],
        "K": ["ε"],
        "W": ["υ"]
    }
    resultado = ""
    for char in texto.upper():
        if char in mapa_cifrado:
            resultado += random.choice(mapa_cifrado[char])
        else:
            resultado += char
    return resultado
    
textoB = """Es verdad; pues reprimamos
esta fiera condicion,
esta furia, esta ambicion,
por si alguna vez sonamos.
Y si haremos, pues estamos
en mundo tan singular,
que el vivir solo es sonar;
y la experiencia me ensena
que el hombre que vive suena
lo que es, hasta despertar.

Suena el rey que es rey, y vive
con este engano mandando,
disponiendo y gobernando;
y este aplauso, que recibe
prestado, en el viento escribe,
y en cenizas le convierte
la muerte, ¡desdicha fuerte!
Que hay quien intente reinar,
viendo que ha de despertar
en el sueno de la muerte.

Suena el rico en su riqueza,
que mas cuidados le brinda
que el bien que de ella se saca,
y el que mas la estimar solia,
con solo ver que se acaba
desengañado se queja;
suena el que mas vil se deja
por honra de su parentela,
y el que en libertad vivia
somete al yugo su cabeza.

Suena el que a sus pensamientos
daba ley y gobernacion,
y el que a su voluntad ponia
todo el mundo a su alcance;
suena el que en gran abundancia
tenia oro, bienes y suerte,
y el que en su pobreza fuerte
soporta con paciencia;
suena todo, y la evidencia
desengana toda muerte."""

textoA = """En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho
tiempo que vivia un hidalgo de los de lanza en astillero, adarga antigua, rocin flaco
y galgo corredor. Una olla de algo mas vaca que carnero, salpicon las mas noches,
duelos y quebrantos los sabados, lantejas los viernes, algun palomino de anadidura
los domingos, consumian las tres partes de su hacienda. El resto della concluian
sayo de velarte, calzas de velludo para las fiestas, con sus pantuflos de lo mesmo, y
los dias de entresemana se honraba con su vellori de lo mas fino. Tenia en su casa
una ama que pasaba de los cuarenta, y una sobrina que no llegaba a los veinte, y un
mozo de campo y plaza, que asi ensillaba el rocin como tomaba la podadera. Frisaba
la edad de nuestro hidalgo con los cincuenta anos; era de complexion recia, seco
de carnes, enjuto de rostro, gran madrugador y amigo de la caza. Quieren decir
que tenia el sobrenombre de Quijada, o Quesada, que en esto hay alguna diferencia
en los autores que deste caso escriben; aunque, por conjeturas verosimiles, se deja
entender que se llamaba Quejana. Pero esto importa poco a nuestro cuento; basta
que en la narracion del no se salga un punto de la verdad.
Es, pues, de saber que este sobredicho hidalgo, los ratos que estaba ocioso, que eran
los mas del ano, se daba a leer libros de caballerias, con tanta aficion y gusto, que
olvido casi de todo punto el ejercicio de la caza, y aun la administracion de su
hacienda. Y llego a tanto su curiosidad y desatino en esto, que vendio muchas
hanegas de tierra de sembradura para comprar libros de caballerias en que leer,
y asi, llevo a su casa todos cuantos pudo haber dellos; y de todos, ningunos le
parecian tan bien como los que compuso el famoso Feliciano de Silva, porque la
claridad de su prosa y aquellas entricadas razones suyas le parecian de perlas, y
mas cuando llegaba a leer aquellos requiebros y cartas de desafios, donde en muchas
partes hallaba escrito: La razon de la sinrazon que a mi razon se hace, de tal
manera mi razon enflaquece, que con razon me quejo de la vuestra fermosura. Y
tambien cuando leia: ...los altos cielos que de vuestra divinidad divinamente con
las estrellas os fortifican, y os hacen merecedora del merecimiento que merece la
vuestra grandeza."""



print(cifrar_cesar(textoB, 5))
print(cifrar_homofonos(textoB))


