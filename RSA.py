from utils import *

def generate_keys(keySize):
    """
    keySize:n no of bits 
    """

    # Public key is a special Prime 😮
    e=65537
    p=1
    q=0

    totient=0
    while (gcd(totient,e)!=1 and p!= q):
        # When you multiply two numbers, the number of bits in the product cannot be less than max(m,n) and cannot be more than (m+n)
        p = number.getPrime(math.ceil(keySize/2))
        q = number.getPrime(math.ceil(keySize/2))
       
        n = p*q    # Modulus n = prime*prime =semi prime
        totient = (p-1)*(q-1)
    # Note Public key is <e,n> :D

    # 2.Generating Private Key
    # Private key(d) must satisfy d*e mod n =1 i.e d*e = 1 + k * totient
    d = modInverse(e, totient)
    # Note Public key is <d> :D

    return e,d,n


def encrypt(m, e, n):
    """
    m:plain text number
    e:public key
    n:totient
    """
    # c = m^e mod n
    # Fast Exponential
    c = pow(m, e,n)
    return c


def decrypt(c, d, n):
    """
    c:cipher text
    d:private key
    n:totient
    """
    # Fast Exponential
    m=pow(c,d,n)
    return m


# Ref https://www.nku.edu/~christensen/Mathematical%20attack%20on%20RSA.pdf

def breakRSA(e, n):
    # By knowing n , e(public key) (<e,n> public key pair) trying to attack RSA

    # Brute Force Factorization
    # p,q=brute_force_factorization(n)

    # Fermat's Factorization
    # p,q=fermat_factorization(n)
    # print("p_",p,"q",q)

    # Pollard’s p-1 Algorithm for Prime Factorization
    # p=pollard_p_1_factorization(n)
    # q=n//p

    # Pollard’s Rho Algorithm for Prime Factorization
    p=pollard_rho_factorization(n)
    q=n//p

    totient=(p-1)*(q-1)

    # Built in factorint
    # prime_factors=factorint(n,use_trial=False,use_rho=False)
    # Getting d
    # totient=1
    # # print(prime_factors)
    # for x in prime_factors:
    #     totient = totient*(x-1)

    return modInverse(e, totient)


def brute_force_factorization(n):
    """
    The brute force attack is to try division by all positive integers less than or equal to n .
    since n is a product of 2 prime numbers then it is composite then one of its factors is less than or equal root(n)

    then we can try all numbers from 1 till root(n)
    improvement(1): try only odd numbers bec the only even prime is 2 so no need to try even numbers the aren't prime
    + no need to try 2 because we choose p and q to be large 😮

    improvement(2): try only the primes using next prime instead of trying all odd numbers which may be prime this decrease computations a lot because as it is known that
    as numbers increase the space between primes increase so
    """

    # Special Case(1) n=1
    if (n == 1):
        return n
    
    # Special Case(1) n is even
    if (n % 2 == 0):
        return 2

    # initial value for 3
    p=3


    # This loop is worst case till p<=math.sqrt(n)
    while(n%p!=0):
        # p isn't a factor of n
        # 1.Get next prime
        p=nextprime(p)

    if(n%p==0):
        return p,n//p


def fermat_factorization(n):
    """
    Get the 2 Prime Factors of n 
    Based n the idea of difference of 2 squares 
    Any number of the form pq, where p and q are prime numbers greater than 2, can be written as the difference of two squares

    Fermat's factorization algorithm works well if the factors are roughly the same size.  [Which is our Case here because we make p and q same size ☺]
    """
    # Algorithm:
    # - We have n =p*q but we don't have p or q if we could achieve p&q we could compute d(private key) as follows
    # d*e ≡ 1 mod ((p-1)(q-1))  😎😎

    # - So my aim is to get p and q
    # - we can rewrite n as n=a^2-b^2 =(a-b)(a+b)
    # - b^2=a^2-n so by brute force try different a till we got a perfect number b^2
    # - initially we can say a^2=ceil(sqrt(n))+1

    # Special Case(1) n=1
    if (n == 1):
        return n,n
    
    # Special Case(1) n is even
    if (n % 2 == 0):
        return 2,n//2
    
    a = math.isqrt(n)+1
    # b=0
    # while (a+b-1<=((a+b-1)*(a-b-1))):
    while (True):
        temp = a**2-n
        if (math.isqrt(temp)**2 == temp):
            # If temp is a perfect square then we are done
            b = (int)(math.sqrt(temp))
            break
        a = a+1

    return a+b,a-b


def pollard_p_1_factorization(n):
    """
    Gets prime factorization of large n=pq we aim to get p &q 
    """

    # if a , p are relatively prime gcd(a,p)=1
    # so ferment's theorem a^p-1 ≡ 1 mod p

    # Suppose p-1 is a factor of int L then L=(p-1)*k where k is int
    # a^L ≡ a^(p-1)*k  mod p 
    # a^L ≡ 1^k mod p ==> a^L ≡ 1 mod p

    # So, p|(a^L-1)  && p|n since n=pq
    # So, gcd(a^L - 1,n) include p (ex 2|10  2|20 gcd(10,20)=2*....)
    # so if we could find L then we can find p 😎 How??

    # Pollard's p-1 Algorithm
    # we aim to find a factor of n
    # 1.Evaluate a^k!    for k=1,2,3,4,....... and gcd(a,n)=1
    # 2.gcd((a^k! -1)mod n,n)
    # 3.Any non trivial(!=1,n) gcd is a factor of n


    # Special Case(1) n=1
    if (n == 1):
        return n
    
    # Special Case(1) n is even
    if (n % 2 == 0):
        return 2


    # choosing base a st gcd(a,n)=1
    a=2
    # if(a%2==0):
    #     a=3
    
    k=1
    fact=1#variable to compute factorial recursively 😁

    while(True):
        # trying ks

        # Fast Exponential
        # (a^k! -1)mod n
        fact=k*fact
        m=pow(a,fact,n)
        gcd_value=math.gcd(m-1, n)
        if(gcd_value>1 and gcd_value<n):
            # non trivial gcd
            # a factor is found
            break
        k+=1
    
    # we got p=gcd 😉
    p=gcd_value
    
    return p


def pollard_rho_factorization(n):
    """
    Gets a prime factorization of n
    """

    # Special Case(1) n=1
    if (n == 1):
        return n
    
    # Special Case(1) n is even
    if (n % 2 == 0):
        return 2
    
    # 1.Choose an easily evaluated function field of integers mod n
    # f(x)=x^2+c  [c=>constant] NB: we are in module N
    c = (random.randint(0, 1) % (n - 1))

    #2. Init T and H random from [2,N) since we are in module N
    T=random.randint(0, 2) % (n - 2)
    H=T

    #2. Obtain Factor
    factor=1
    while(factor==1):
        #2.1. Tortoise Move T(i+1)=f(T(i))
        T=(pow(T,2,n)+c)%n

        #2.2. Hare step H(i+1)=f(f(H(i)))
        H=(pow(H,2,n)+c)%n
        H=(pow(H,2,n)+c)%n

        #2.3. GCD between T-H and n
        factor=gcd(abs(T-H),n)

        #2.4 Check if the Algorithm Failed
        if(factor==n):
            # Retry Again with different c and To and Ho
            return pollard_rho_factorization(n)

    return factor       




# start=time.time()
# brute_force_factorization(6699557)
# end=time.time()
# print(end-start)

# start=time.time()
# fermat_factorization(6699557)
# end=time.time()
# print(end-start)

# start=time.time()
# pollard_p_1_factorization(6699557)
# end=time.time()
# print(end-start)

# start=time.time()
# pollard_rho_factorization(6699557)
# end=time.time()
# print(end-start)