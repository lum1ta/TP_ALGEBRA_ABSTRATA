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

#versão iterativa do algoritmo de euclides porque gasta menos memória
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
        #essa versão não armazena o r simplesmente porque eu não vou usar

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
def teste_miller(k,cont,c):

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
    
    media = soma_tentativas/10

    est = math.log(2**k)/2
    aproximacao = 0.347 * k

    print(f"\nResultados para {k} bits:")
    print(f"Média observada: {media:.2f}")
    print(f"Estimativa teórica ln(2^k)/2: {est:.2f}")
    print(f"Aproximação 0,347k: {aproximacao:.2f}")
#============================================================================
def testar_miller_rabin():

    exemplos = [
        101,          # primo
        1009,         # primo
        91,           # 7*13
        561,          # número de Carmichael
        2047          # pseudoprimo para algumas bases
    ]

    for n in exemplos:
        if eh_primo(n):
            print(f"{n} -> provavelmente primo")
        else:
            print(f"{n} -> composto")

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
    while legendre(z,p) != p - 1:
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
def testar_falha():

    print("\nCaso sem solução:")

    try:
        testar_exemplo(3,41)

    except ValueError as e:
        print(e)
def testar_exemplo(a,p):

    r1 = tonelli(a,p)
    r2 = p - r1

    print(f"\nResolvendo x² ≡ {a} (mod {p})")
    print(f"Raiz 1 = {r1}")
    print(f"Raiz 2 = {r2}")

    print(f"r1² mod p = {(r1*r1)%p}")
    print(f"r2² mod p = {(r2*r2)%p}")

    print(f"r1 + r2 = {r1+r2}")

#=================RSA=======================
#ja tenho o euclides estendido
#ja tenho o mmc
#tenho a exponenciacao modular

#Vamos para as chaves agora

#diferentes primos 
def gera_chave(k):

    #minha função é uma tupla
    _,p = contador(k)
    _,q = contador(k)

    #garante que eles são diferentes
    while(p == q):
        _,p = contador(k)
        _,q = contador(k)
    
    n = p*q
    
    #função totiente de euler requista para o trabalho
    totient = (p - 1)*(q - 1)
    
    while(True):
        e = random.randrange(2,totient)

        if mdc(e,totient) == 1:
            break;
    
    #calcular d,que será o inverso modular de e
    g, d, _ = e_estendido(e, totient)
    assert g == 1

    #caso do d ser negativo
    d = d % totient
    return (n,e),(n,d),p,q #retorn a chave pública e privada

#Função que cifra
def cifra(m,e,n):
    c = mod_pow(m,e,n)
    return c

def decifra(c,d,n):
    return mod_pow(c,d,n)

def assinar(m,d,n):
    return mod_pow(m,d,n)

def verificar_assinatura(s,e,n):
    return mod_pow(s,e,n)

#teste tonelli shanks
def teste_residuos_quadraticos(p):

    print("\n=== Teste de Resíduos Quadráticos ===")

    encontrados = 0

    while encontrados < 5:

        a = random.randint(1, p - 1)

        if legendre(a, p) == 1:

            r = tonelli(a, p)

            print(f"a = {a}")
            print(f"raiz = {r}")
            print(f"verificação = {(r*r)%p}")

            encontrados += 1

#teste de corretude
def teste_rsa(k):

    chave_publica, chave_privada, p, q = gera_chave(k)

    n, e = chave_publica
    _, d = chave_privada

    print("\nChave pública:")
    print(f"n = {n}")
    print(f"e = {e}")

    print("\nChave privada:")
    print(f"d = {d}")

    print("\n=== Teste RSA ===")

    for i in range(20):

        m = random.randint(1, n - 1)

        # cifração
        c = cifra(m, e, n)

        # decifração
        m_rec = decifra(c, d, n)

        if m_rec != m:
            raise ValueError("Falha na cifração RSA")

        # assinatura
        s = assinar(m, d, n)

        # verificação
        m_verificado = verificar_assinatura(s, e, n)

        if m_verificado != m:
            raise ValueError("Falha na assinatura digital")

        print(f"Teste {i+1}: OK")

    print("Todos os testes RSA passaram.")

    teste_residuos_quadraticos(p)


#=================== MAIN ===================

def main():

    print("IMPLEMENTAÇÃO DE MILLER-RABIN + TONELLI-SHANKS + RSA")

    # T7 - Miller-Rabin
    print("\n[T7] Geração de Primos com Miller-Rabin")

    teste_miller()

    print("\nExemplos adicionais:")

    testar_miller_rabin()

    # T4 - Tonelli-Shanks
    print("\n[T4] Exemplos obrigatórios")

    testar_exemplo(5, 41)
    testar_exemplo(2, 113)
    testar_falha()

    # T9 - RSA
    print("\n[T9] RSA")

    k = pegar_k()

    teste_rsa(k)

    print("\nTodos os testes concluídos com sucesso.")


if __name__ == "__main__":
    main()