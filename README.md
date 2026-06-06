# README

## Requisitos

* Python 3 instalado (versão 3.8 ou superior).

As bibliotecas utilizadas (`random`, `math` e `sys`) já fazem parte da biblioteca padrão do Python.

## Como executar

No terminal, navegue até a pasta onde está o arquivo `rsa.py` e execute:

```bash
python rsa.py
```

ou

```bash
python3 rsa.py
```

## O que o programa faz

O programa implementa:

* Teste de primalidade Miller–Rabin;
* Geração de números primos de 32, 64 ou 128 bits;
* Algoritmo de Tonelli–Shanks para cálculo de raízes quadradas modulares;
* Criptossistema RSA completo (geração de chaves, cifração, decifração e assinatura digital).

## Entrada

Durante a execução, será solicitado o tamanho dos primos utilizados no RSA:

```text
Defina o número de bits do candidato gera (32,64 ou 128):
```

Digite uma das opções:

```text
32
64
128
```

## Saída

O programa executa automaticamente:

1. Testes do algoritmo Miller–Rabin;
2. Exemplos do algoritmo Tonelli–Shanks;
3. Geração de chaves RSA;
4. Testes de cifração, decifração e assinatura digital.

Ao final, será exibida a mensagem:

```text
Todos os testes concluídos com sucesso.
```
