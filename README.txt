README.txt

IMPLEMENTAÇÃO DE MILLER–RABIN, TONELLI–SHANKS E RSA

========================================
REQUISITOS

* Python 3.8 ou superior.
* Não é necessária a instalação de bibliotecas externas.

======================================
EXECUÇÃO


No terminal, execute:

python rsa.py

ou

python3 rsa.py

O programa executará automaticamente os testes dos tópicos implementados.

======================================
TÓPICO 7 - GERAÇÃO DE PRIMOS (MILLER-RABIN)

O programa gera números primos de 32, 64 e 128 bits utilizando o teste de Miller–Rabin.

Exemplo de saída:

Execução 1: 12 tentativas (primo encontrado: ...)
Execução 2: 18 tentativas (primo encontrado: ...)
...

Também são executados testes em números conhecidos:

101
1009
91
561
2047

Exemplo de resultado:

101 -> provavelmente primo
91 -> composto

========================================
TÓPICO 4 - RAIZ QUADRADA MODULAR (TONELLI-SHANKS)

São executados automaticamente os exemplos exigidos pelo trabalho:

x² ≡ 5 (mod 41)

x² ≡ 2 (mod 113)

Exemplo de saída:

Resolvendo x² ≡ 5 (mod 41)
Raiz 1 = ...
Raiz 2 = ...

Também é executado um caso sem solução para verificar a detecção de não-resíduos quadráticos.

========================================
TÓPICO 9 - RSA

Ao iniciar os testes RSA, o programa solicita:

Defina o número de bits do candidato gera (32,64 ou 128):

Exemplo:

64

O programa então:

* Gera dois primos utilizando Miller–Rabin;
* Calcula as chaves pública e privada;
* Realiza testes de cifração e decifração;
* Realiza testes de assinatura e verificação.

Exemplo de saída:

Chave pública:
n = ...
e = ...

Chave privada:
d = ...

Teste 1: OK
Teste 2: OK
...
Teste 20: OK

Todos os testes RSA passaram.

========================================
OBSERVAÇÃO
==========

Os resultados numéricos mudam a cada execução, pois os algoritmos utilizam números aleatórios para geração de candidatos primos e chaves RSA.
