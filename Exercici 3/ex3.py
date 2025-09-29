# Programa que descobreix claus de Vigenère en text xifrat i retorna el text desxifrat

import re
from collections import Counter, defaultdict
from math import gcd
from itertools import product

def find_vigenere_keys(ciphertext, max_key_len=10, top_n=5):
    """
    Descubre claves de un Vigenère en texto cifrado.
    Devuelve:
      - lista con las top_n claves candidatas
      - el descifrado con la primera clave (la más probable)
    """
    # === Datos auxiliares ===
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    CAT_FREQ = {
        'A': 0.125, 'B': 0.015, 'C': 0.038, 'D': 0.045, 'E': 0.118, 'F': 0.008, 'G': 0.017, 'H': 0.009,
        'I': 0.075, 'J': 0.003, 'K': 0.001, 'L': 0.055, 'M': 0.038, 'N': 0.068, 'O': 0.079, 'P': 0.028,
        'Q': 0.010, 'R': 0.060, 'S': 0.080, 'T': 0.055, 'U': 0.042, 'V': 0.010, 'W': 0.0005, 'X': 0.004,
        'Y': 0.001, 'Z': 0.001
    }
    COMMON_CAT_WORDS = ["DE","LA","QUE","I","EL","EN","PER","NO","UN","UNA","ALS","AMB","ES","PEL","LES","ELS","DEL","COM"]

    def sanitize(text):
        return re.sub('[^A-Za-z]', '', text).upper()

    def index_of_coincidence(text):
        N = len(text)
        if N <= 1:
            return 0.0
        freqs = Counter(text)
        return sum(v*(v-1) for v in freqs.values()) / (N*(N-1))

    def vigenere_decrypt_clean(ct, key):
        res = []
        for i, ch in enumerate(ct):
            ci = ord(ch) - ord('A')
            ki = ord(key[i % len(key)]) - ord('A')
            pi = (ci - ki) % 26
            res.append(chr(pi + ord('A')))
        return ''.join(res)

    def vigenere_decrypt_with_format(ciphertext, key):
        """Descifra preservando espacios, puntuación y mayúsculas/minúsculas."""
        res = []
        j = 0  # índice en la clave
        for ch in ciphertext:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                ci = ord(ch.upper()) - ord('A')
                ki = ord(key[j % len(key)]) - ord('A')
                pi = (ci - ki) % 26
                res.append(chr(pi + base))
                j += 1
            else:
                res.append(ch)
        return ''.join(res)

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
        ics = [index_of_coincidence(col) for col in cols if len(col) > 0]
        return sum(ics)/len(ics) if ics else 0.0

    def best_key_for_length(ct, keylen):
        cols = [''.join(ct[i::keylen]) for i in range(keylen)]
        key = ""
        for col in cols:
            col_count = Counter(col)
            col_len = len(col)
            best_shift = 0
            best_score = -1e9
            for shift in range(26):
                score = 0.0
                for ch, cnt in col_count.items():
                    plain_ord = (ord(ch)-ord('A') - shift) % 26
                    plain_letter = chr(plain_ord + ord('A'))
                    score += (cnt/col_len) * CAT_FREQ.get(plain_letter, 0)
                if score > best_score:
                    best_score = score
                    best_shift = shift
            key += chr(best_shift + ord('A'))
        return key

    def score_plaintext(pt):
        score = 0.0
        up = pt.upper()
        for w in COMMON_CAT_WORDS:
            score += up.count(w) * 2.0
        ic = index_of_coincidence(pt)
        score += -abs(ic - 0.075) * 50.0
        vowel_count = sum(up.count(v) for v in "AEIOU")
        score += (vowel_count / max(1, len(up))) * 10.0
        return score

    # === Proceso ===
    clean_ct = sanitize(ciphertext)
    if len(clean_ct) == 0:
        return [], ""

    spacings = []
    for L in range(3,6):
        spacings += repeated_sequences_spacings(clean_ct, seq_len=L)
    gcd_guess = gcd_list(spacings)

    ic_scores = [(k, avg_ic_for_keylen(clean_ct, k)) for k in range(1, max_key_len+1)]
    ic_scores_sorted = sorted(ic_scores, key=lambda x: -x[1])
    candidate_lengths = set([k for k,_ in ic_scores_sorted[:5]])
    if gcd_guess:
        for d in range(1, max_key_len+1):
            if gcd_guess % d == 0:
                candidate_lengths.add(d)
        candidate_lengths.add(gcd_guess)
    candidate_lengths = sorted([k for k in candidate_lengths if 1 <= k <= max_key_len])

    results = []
    for keylen in candidate_lengths:
        key_candidate = best_key_for_length(clean_ct, keylen)
        plaintext_candidate = vigenere_decrypt_clean(clean_ct, key_candidate)
        sc = score_plaintext(plaintext_candidate)
        results.append({"key": key_candidate, "score": sc})

    results_sorted = sorted(results, key=lambda x: -x['score'])
    seen, final = set(), []
    for r in results_sorted:
        if r['key'] in seen:
            continue
        seen.add(r['key'])
        final.append(r["key"])
        if len(final) >= top_n:
            break

    best_plain = vigenere_decrypt_with_format(ciphertext, final[0]) if final else ""

    return final, best_plain

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

print(find_vigenere_keys(texto_cifrado, max_key_len=10, top_n=3))