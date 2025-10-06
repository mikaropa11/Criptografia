# Programa que estima la longitud de la clau d'un text xifrat amb Vigenère

import re
from collections import Counter, defaultdict
from math import gcd

def estimate_key_length(ciphertext, max_key_len=30):
    def sanitize(text):
        return re.sub('[^A-Za-z]', '', text).upper()

    def index_of_coincidence(text):
        N = len(text)
        if N <= 1:
            return 0.0
        freqs = Counter(text)
        return sum(v*(v-1) for v in freqs.values()) / (N*(N-1))

    def repeated_sequences_spacings(ct, seq_len=3):
        seq_locs = defaultdict(list)
        for i in range(len(ct) - seq_len + 1):
            seq = ct[i:i+seq_len]
            seq_locs[seq].append(i)
        spacings = []
        for locs in seq_locs.values():
            if len(locs) > 1:
                for i in range(len(locs)-1):
                    spacings.append(locs[i+1] - locs[i])
        return spacings

    def gcd_list(nums):
        nums = [n for n in nums if n>0]
        if not nums:
            return None
        g = nums[0]
        for n in nums[1:]:
            g = gcd(g, n)
        return g

    def avg_ic_for_keylen(ct, keylen):
        cols = [''.join(ct[i::keylen]) for i in range(keylen)]
        ics = [index_of_coincidence(col) for col in cols if len(col) > 1]
        return sum(ics)/len(ics) if ics else 0.0

    ct = sanitize(ciphertext)
    if len(ct) < 20:
        return None

    # 1) Kasiski
    spacings = []
    for L in range(3,6):
        spacings += repeated_sequences_spacings(ct, seq_len=L)
    gcd_guess = gcd_list(spacings)

    # 2) Índice de coincidencia
    ic_scores = [(k, avg_ic_for_keylen(ct, k)) for k in range(2, max_key_len+1)]
    ic_sorted = sorted(ic_scores, key=lambda x: abs(x[1]-0.074))  # Catalán ≈ 0.074

    # Elegimos la mejor candidata descartando longitud 1
    best_k = ic_sorted[0][0]
    if gcd_guess and gcd_guess != 1:
        return gcd_guess if ic_sorted[0][0] != gcd_guess else ic_sorted[0][0]
    return best_k


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

print("La longitud estimada és de:", estimate_key_length(texto_cifrado))