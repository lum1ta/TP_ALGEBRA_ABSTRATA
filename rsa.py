#Pretendo implementar um RSA próprio com os métodos requisitados com o teste de miller rabin e um tonelli-shamks para verificar os residuos quadraticos

#%%===============BIBLIOTECAS UTILIZADAS===============
import random
import sys
import math
#%%=======FUCOES MATEMATICAS=======

#exponenciação modular
#é pra retornar x^ŷ %p
#vou usar isso aqui no RSA
def mod_pow(x,y,p):

    #Inicializar o resultado
    res = 1 

    #atualizar a base se ela for maior ou igual a p
    x = x  % p
    while(y > 0):

        #se y for par
        if(y & 1):
            res = (res * x) % p

        #agora y deve ser par
        y = y >> 1
        x = (x * x) % p
    return res

def mdc(a,b):
    if (b == 0):
        return a
    else:
        return mdc(b, a % b)

def e_estendido(a,b):
    x, v_x = 0,1
    y, v_y = 1,0

    while(b != 0):
        quo = a // b
        a, b = b, a - quo * b
        v_x, x = x, v_x - quo * x
        v_y, y = y, v_y - quo* y

    return a, v_x, v_y
 #%%=====GERA O K BASE PARA TUDO NO CÓDIGO======
def pegar_k():
    k = int(input("Defina o número de bits do candidato gera (32,64 ou 128):"))
    if k not in (32, 64, 128):
        sys.exit(1)
    return k

#%%=======PRIMALIDADE===============
#gera candidato
def gera_candidato(k):

    #gera o numero
    n = random.getrandbits(k)

    #verificacao de k bits
    n |= (1 << (k - 1) )

    #verficacao que é impar
    n |= 1 #força o ultimo bit a ser 1 com uma operacao OR

    return n 

# teste de miller rabin para teste de primos

def miller_rabin(d,n):

    #segurado pelo teorema de fermat

    a = 2 + random.randint(0, n -  4)


    x = mod_pow(a,d,n)

    if(x == 1 or x== (n - 1)):
        return True

    # x é elevado até que uma das condições não aconteça:
    # (i) d nao pode ser n-1
    # (ii) (x^2) % n != 1
    # (iii) (x^2) % n != n-1
    #segurado pelo teorema de fermat

    while(d != n - 1):
        x = (x * x) % n
        d *= 2
        #eu acho que amarmazenar or vai ser importante para verificar reisduo quadraticos nos
        #ataques mas ainda não estudei essa parte

        if (x == 1):
            return False;
        if (x == n - 1):
            return True;

    return False

#responde só se é primo ou não
def eh_primo(n,k = 11):
    
    #os casos que o algoritmo não cobre
    if(n <= 1 or n == 4):
        return False
    
    if(n <= 3):
        return True
    
    #tem que ter um r que n−1 = 2r⋅d(PTF)
    d = n - 1;
    while (d % 2 == 0):
        d //= 2;

    for i in range(k):
        
        if (miller_rabin(d, n) == False):
            return False;

    return True;

def contador(k):
    cont = 0

    while True:
        c = gera_candidato(k)
        cont += 1

        if eh_primo(c, k=11):
            return cont, c

#Finalmente posso ir para as experimentações agora ebaa
#===========================EXPERIMENTAÇÃO DA T7===================================================================
def teste(k,cont,c):

    for k in (32,64,128):
        soma_tentativas = 0

        for exe in range(1,11):
            tentativas,primo = contador(k)
            soma_tentativas += tentativas
        
        print(
            f"Execução {exe}: "
            f"{tentativas} tentativas "
            f"(primo encontrado: {primo})"
        )
    
    media = tentativas/10

    est = math.log(2**k)/2
    aproximacao = 0.347 * k

    print(f"\nResultados para {k} bits:")
    print(f"Média observada: {media:.2f}")
    print(f"Estimativa teórica ln(2^k)/2: {est:.2f}")
    print(f"Aproximação 0,347k: {aproximacao:.2f}")
#============================================================================

#%%=============TONELLI SHANKS==================

#verificação de solubilidade
def legendre(a ,p):
    #critério de euler
    return pow(a ,( p - 1) // 2,p)

#tonelli de fato
def tonelli(n,p):
    
    if legendre(n,p) != 1:
        raise ValueError("Não é resíduo quadrático")
    #tenho que achar um q e um s tal que p - 1 = Q2^s

    if n == 0:
        return 0
    
    if p == 2:
        return n
    
    if p % 4 == 3:
        return pow(n ,( p + 1) // 4,p)
    
    q = p - 1
    s = 0

    while (q % 2 == 0):
        q //= 2
        s += 1
    z = 2
    while legendre(z,p) != p - 1
        z += 1

    c = pow(z,q,p)
    t = pow(n,q,p)
    R = pow(n,(q +1) // 2,p)
    m = s
        
    while t != 1 :

        t2 = t

        for i in range(m):
            if t2 == 1:
                break;
            t2 = pow(t2,2,p)
        b = pow(c, 1 << (m - i - 1), p)
        R = (R * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return R

def verificar_raizes(a,p):

    r1 = tonelli(a,p)
    r2 = p - r1

    print("Raiz 1 =", r1)
    print("Raiz 2 =", r2)

    print("Soma =", r1+r2)

    assert (r1*r1) % p == a % p
    assert (r2*r2) % p == a % p
    assert r1 + r2 == p

def testar_exemplo(a,p):

    r1 = tonelli(a,p)
    r2 = p - r1

    print(f"\nResolvendo x² ≡ {a} (mod {p})")
    print(f"Raiz 1 = {r1}")
    print(f"Raiz 2 = {r2}")

    print(f"r1² mod p = {(r1*r1)%p}")
    print(f"r2² mod p = {(r2*r2)%p}")

    print(f"r1 + r2 = {r1+r2}")

# exemplos obrigatórios
testar_exemplo(5,41)
testar_exemplo(2,113)