import re 
from collections import Counter
from ex3a import estimate_key_length

# Frecuencia típica del catalán (aproximada, en porcentaje)
CATALAN_FREQ = {
    'A': 12.53, 'B': 1.41, 'C': 4.16, 'D': 4.86, 'E': 12.36, 'F': 0.68,
    'G': 1.74, 'H': 0.70, 'I': 6.88, 'J': 0.44, 'L': 4.97, 'M': 3.15,
    'N': 7.01, 'O': 8.54, 'P': 2.91, 'Q': 1.02, 'R': 6.56, 'S': 8.05,
    'T': 4.57, 'U': 4.46, 'V': 1.00, 'X': 1.22, 'Y': 0.14, 'Z': 0.52
}

def sanitize(text):
    return re.sub('[^A-Za-z]', '', text).upper()

def shift_letter(letter, shift):
    return chr((ord(letter) - ord('A') - shift) % 26 + ord('A'))

def chi_squared_statistic(text):
    N = len(text)
    if N == 0:
        return float('inf')
    observed_counts = Counter(text)
    chi2 = 0.0
    for letter in CATALAN_FREQ:
        observed = observed_counts.get(letter, 0)
        expected = CATALAN_FREQ[letter] * N / 100
        chi2 += ((observed - expected) ** 2) / expected if expected != 0 else 0
    return chi2

def find_key(ciphertext, key_length):
    ct = sanitize(ciphertext)
    key = ""
    for i in range(key_length):
        subalphabet = ct[i::key_length]
        min_chi2 = float('inf')
        best_shift = 0
        for shift in range(26):
            decrypted = ''.join(shift_letter(c, shift) for c in subalphabet)
            chi2 = chi_squared_statistic(decrypted)
            if chi2 < min_chi2:
                min_chi2 = chi2
                best_shift = shift
        key += chr(ord('A') + best_shift)
    return key

texto_cifrado = """tl fmmcse dilwhkb mg qgiibhocaeqlw iafjx qdnxonh rof i xlpmxv ws zalqlyx o izhjp dx
stgxsdq xg jn fmmcse imk oiavik sas qqyfptzml rt snjlhxtnkbc eoeqtzuaummwra vwf sa
xbnkoigx lx jxgxvxft
ajcxgi mxbhrt dxc xz hen vha p lhnbqxae xkihsbi yfxewzbqw ktabgzi jcx sa vt xnpaivik sa
1863 pxzh gtmutt vpvxz xgiam lxgroumkh se figsga bvwseeglxbi pxz vvpreml ppbuizs ya xt
1846
xb tll fbtgamoxg se lcugiimcvwd phtboaftjxhxcl wg sas ttyoqema ws huuamwiuvqh sh tkqxb
bimrtbtagb eih d’nvt dprtceo rltc esmafmg rt ktabgzi imkatt t cg qgiibhocaeqlhp dxlnwg lt
thbvimcw rt lt xtfpuei vzpu
nv vce dxavcqekbt zp lhvzwiuw lx zp ptztiaa vtti tl vzbdiotvtzxsmi tzxnxi xz ieqb qwurtb xb
c chtnacel wg b ts ei eccgbbnr se ei iogantt qaan
ieshhhzxg rawi vcaufvt sh phb mfpcmik qdm xt msmt qqyfpt wcg lxfkim rt snjlhxtnkbe
bogwtzuaunmwra
vwf o iae ktrp chtnaca iwm gtr tbtqpdt ifp pnttbgx dx nksfuxvvwp Dx tt aptxqqo bagmko
futv lvp umqewiztb nbp mtynwca wm qwurtbzs se vwkftnm lx fdthz tejelb fsiowm ici pxzfsirx lxrjik tt zdnzqmis dxtl fdthzl wcdbdbrjaea
dohilsb sh vt iwccak lx ztxbamsccbi ws eakinzts kmisiiwml sc ee bxli xbnkoi ee yns hizvbtxct
otwgeum taq thbt dgouiuwaimim eje tynshtxa iogantxg co gwfsh ekmg zp mtbxwma tjtbh
dxt qwurtb lwco jcx o bel tt qaan khwccblbo tn ei foiebft ddsbkbc tn eml rjel wvigrxvvwts
liusct ettjdrl yns aa wqlhpnvqt sctkm iogantxg geimmwsel ml ajlmqizt dx tt zdnzqmis dx
tt qaan mko fuxamwd dx kxfrak lbttrxvmg eakinzts jcx sh rxxxhxslqg w irhjtf tl lmn apxbu
vcbu wqowhok xxf sajcxgia figsga mzhppr nv fiatbxes erhxxf p lt thbvimcw rt lt keoj
lt thbvimcw rt lt keoj sxzt ofuxam bdmuzx c plzcg tpcmwk dgifmk rpqnmlh
jn vwi rtsvwusgtt tt zdnzqmis dx tt qaan ifp fux ml jp xbnkog ee lhqjmxvm bdmxa voa
dbdbrxr xt msmt xv uzdcl lx zp mtbxwma fqwo fux tt zdnzqmis dx tt qaan q tdaivik sa
mxbhrt elbtrxsmqv hgawqvwdntt wsa xbnkoigx lx qtstz"""

key_length = estimate_key_length(texto_cifrado)
print("La clave estimada es:", find_key(texto_cifrado, key_length))