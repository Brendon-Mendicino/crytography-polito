from Crypto.Util.number import long_to_bytes, isPrime
import math


# def contfrac_to_rational (frac):
#     '''Converts a finite continued fraction [a0, ..., an]
#      to an x/y rational.
#      '''
#     if len(frac) == 0:
#         return (0,1)
#     num = frac[-1]
#     denom = 1
#     for _ in range(-2,-len(frac)-1,-1):
#         num, denom = frac[_]*num+denom, num
#     return (num,denom)

# def rational_to_contfrac(x,y):
#     '''
#     Converts a rational x/y fraction into
#     a list of partial quotients [a0, ..., an]
#     '''
#     a = x//y
#     pquotients = [a]
#     while a * y != x:
#         x,y = y,x-a*y
#         a = x//y
#         pquotients.append(a)
#     return pquotients
    
# def convergents_from_contfrac(frac):
#     '''
#     computes the list of convergents
#     using the list of partial quotients
#     '''
#     convs = [];
#     for i in range(len(frac)):
#         convs.append(contfrac_to_rational(frac[0:i]))
#     return convs
    

# def is_perfect_square(n):
#     '''
#     If n is a perfect square it returns sqrt(n),
    
#     otherwise returns -1
#     '''
#     h = n & 0xF; #last hexadecimal "digit"
    
#     if h > 9:
#         return -1 # return immediately in 6 cases out of 16.

#     # Take advantage of Boolean short-circuit evaluation
#     if ( h != 2 and h != 3 and h != 5 and h != 6 and h != 7 and h != 8 ):
#         # take square root if you must
#         t = math.isqrt(n)
#         if t*t == n:
#             return t
#         else:
#             return -1
    
#     return -1

# def hack_RSA(e,n):
#     '''
#     Finds d knowing (e,n)
#     applying the Wiener continued fraction attack
#     '''
#     frac = rational_to_contfrac(e, n)
#     convergents = convergents_from_contfrac(frac)
    
#     for (k,d) in convergents:
        
#         #check if d is actually the key
#         if k!=0 and (e*d-1)%k == 0:
#             phi = (e*d-1)//k
#             s = n - phi + 1
#             # check if the equation x^2 - s*x + n = 0
#             # has integer roots
#             discr = s*s - 4*n
#             if(discr>=0):
#                 t = is_perfect_square(discr)
#                 if t!=-1 and (s+t)%2==0:
#                     print("Hacked!")
#                     return d

from typing import Tuple, Iterator, Iterable, Optional


def isqrt(n: int) -> int:
    """
    ref: https://en.wikipedia.org/wiki/Integer_square_root
    
    >>> isqrt(289)
    17
    >>> isqrt(2)
    1
    >>> isqrt(1000000 ** 2)
    1000000
    """
    if n == 0:
        return 0

    # ref: https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Rough_estimation
    x = 2 ** ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def is_perfect_square(n: int) -> bool:
    """
    ref: https://hnw.hatenablog.com/entry/20140503

    >>> is_perfect_square(100)
    True
    
    >>> is_perfect_square(2000000000000000000000000000 ** 2)
    True

    >>> is_perfect_square(2000000000000000000000000000 ** 2 + 1)
    False
    """
    sq_mod256 = (1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
    if sq_mod256[n & 0xff] == 0:
        return False

    mt = (
        (9, (1,1,0,0,1,0,0,1,0)),
        (5, (1,1,0,0,1)),
        (7, (1,1,1,0,1,0,0)),
        (13, (1,1,0,1,1,0,0,0,0,1,1,0,1)),
        (17, (1,1,1,0,1,0,0,0,1,1,0,0,0,1,0,1,1))
    )
    a = n % (9 * 5 * 7 * 13 * 17)
    if any(t[a % m] == 0 for m, t in mt):
        return False

    return isqrt(n) ** 2 == n


def rational_to_contfrac(x: int, y: int) -> Iterator[int]:
    """
    ref: https://en.wikipedia.org/wiki/Euclidean_algorithm#Continued_fractions
    
    >>> list(rational_to_contfrac(4, 11))
    [0, 2, 1, 3]
    """
    while y:
        a = x // y
        yield a
        x, y = y, x - a * y


def contfrac_to_rational_iter(contfrac: Iterable[int]) -> Iterator[Tuple[int, int]]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf (6)
    """
    n0, d0 = 0, 1
    n1, d1 = 1, 0
    for q in contfrac:
        n = q * n1 + n0
        d = q * d1 + d0
        yield n, d
        n0, d0 = n1, d1
        n1, d1 = n, d


def convergents_from_contfrac(contfrac: Iterable[int]) -> Iterator[Tuple[int, int]]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf Section.3
    """
    n_, d_ = 1, 0
    for i, (n, d) in enumerate(contfrac_to_rational_iter(contfrac)):
        if i % 2 == 0:
            yield n + n_, d + d_
        else:
            yield n, d
        n_, d_ = n, d


def attack(e: int, n: int) -> Optional[int]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf Section.4
    
    >>> attack(2621, 8927)
    5
    >>> attack(6792605526025, 9449868410449)
    569
    >>> attack(30749686305802061816334591167284030734478031427751495527922388099381921172620569310945418007467306454160014597828390709770861577479329793948103408489494025272834473555854835044153374978554414416305012267643957838998648651100705446875979573675767605387333733876537528353237076626094553367977134079292593746416875606876735717905892280664538346000950343671655257046364067221469807138232820446015769882472160551840052921930357988334306659120253114790638496480092361951536576427295789429197483597859657977832368912534761100269065509351345050758943674651053419982561094432258103614830448382949765459939698951824447818497599, 109966163992903243770643456296093759130737510333736483352345488643432614201030629970207047930115652268531222079508230987041869779760776072105738457123387124961036111210544028669181361694095594938869077306417325203381820822917059651429857093388618818437282624857927551285811542685269229705594166370426152128895901914709902037365652575730201897361139518816164746228733410283595236405985958414491372301878718635708605256444921222945267625853091126691358833453283744166617463257821375566155675868452032401961727814314481343467702299949407935602389342183536222842556906657001984320973035314726867840698884052182976760066141)
    4221909016509078129201801236879446760697885220928506696150646938237440992746683409881141451831939190609743447676525325543963362353923989076199470515758399
    """
    f_ = rational_to_contfrac(e, n)
    for k, dg in convergents_from_contfrac(f_):
        edg = e * dg
        phi = edg // k

        x = n - phi + 1
        if x % 2 == 0 and is_perfect_square((x // 2) ** 2 - n):
            g = edg - phi * k
            return dg // g
    return None

n = 138728501052719695830997827983870257879591108626209095010716818754108501959050430927220695106906763908822395818876460759364322997020222845247478635848425558793671347756842735011885094468024344931360037542098264527076663690119553302046205282212602106990248442514444587909723612295871002063257141634196430659767
 
e = 60016485563460433620911462871489753027091796150597697863772440338904706321535832359517415034149374289955681381097544059467926029963755494161141305994584249448583991034102694954139120453335603006006970009433124857766494518747385902016093339683987307620366742481560543776055295663835860818720290861634213881385
 
c = 2322197070893918184798450987261006738974212676868546918116025143689179595012453741443096765746632956074733175884148765942012939757814015701500677535159711784449838737347884966712840037171715387431349326855191231267900494076862957861433755009845773324374237361630377798806043317195038461254707686413550495823
 

d = attack(e, n)
print(d)
 

# phi = math.isqrt(n) - 1 ** 2
# while True:
#     m = pow(c, d, n)
#     dec = long_to_bytes(m)
#     if dec.find(b'CRYPTO') != -1:
#         print(dec)
#         break

#     d -= 1