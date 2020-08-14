# coding at utf-8

# Sessão de importações
import math

def sqrt(x):
    assert x >= 0
    i = 1
    while i**2 <= x:
        i *= 2
    y = 0
    while i > 0:
        if (y + i)**2 <= x:
            y += 1
        i //=2
    return y



### Bisseção
def passo_da_bissecao (f, a, b):
    """Retorna o novo intervalo após uma etapa da bisseção da função f, 
    da forma (a,m) ou (m,b) segundo em qual seja possível garantir uma raiz de f.
    """
    m = (a+b)/2
    if f(m)*f(a) < 0:
        return a, m
    else:
        return m, b

def bissecao (f, a, b, xtol=1e-8, verbose=False):
    """Encontra uma raíz de  f  no intervalo  [a,b].
    
    Se visual=True: Retorna a raiz e uma lista com as extremidades dos intervalos construídos da forma:
    (raíz, [(a_1,b_1), (a_2,b_2), ...])
    
    Se visual=False: Retorna a raíz de  f  no intervalo.
    """    
    intervalos = [(a,b)]
    while abs(b-a) >= xtol: # "invertemos" o teste de parada. agora é teste de continnuada...
        a, b = passo_da_bissecao (f, a, b)
        if verbose:
            intervalos.append((a,b))
    # Se chegamos até aqui, é porque o intervalo está pequeno o suficiente!
    if verbose:
        intervalos.append((a,b))
        return (a+b)/2, intervalos
    else:
        return (a+b)/2
    


### Método de Newton
def passo_newton (df):
    """Retorna o novo valor de  x, aplicando uma aiteração do método de Newton.
    """
    return df(0)

def deriv (f, dh=1e-16):
    """Retorna a aproximação da derivada de  f  em forma de função, dada um  delta h.
    """
    def df(x): 
        """Retorna a aproximação da derivada da função no ponto  x.
        """
        return (f(x) - f(x+dh)) / dh
    return df

def newton (f, x_0, maxiter=1e3, erro_min=1e-16, verbose=False):
    """Aplica o método de Newton na função  f  e retorna a aprox. da raiz (com o erro mínimo erro_min).
    
    Se visual=True: Retorna a raiz e uma lista com x_n alcansados, da forma:
    (raíz, [x_1, x_2, x_3, ...])
    
    Se visual=False: Retorna a raíz de  f.
    """
    x_n = []
    df = deriv(f, erro_min)
    t, x = 0, x_0 # t  é o número de iterações
    while t < maxiter:
        x = passo_newton (df)
        t += 1        
        if verbose:
            x_n.append(x)
    if verbose: return x, x_n
    else: return x



### Sequência de Fibonacci
cache_fib = {}
def fib_recursiva(n):
    """Retorna o n-ésimo elemento da sequência de Fibonacci.
    """
    assert n >= 0 and isinstance(n, int), "Estamos trabalhando com fib positivo."
    
    #memoização
    if n in cache_fib:
        return cache_fib[n]
    
    #caso-base
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    #recursão
    result = fib_recursiva(n-1) + fib_recursiva(n-2)
    cache_fib[n] = result
    return result

def take(n, g):
    """Gera até os n primeiros elementos do gerador g."""
    if n <= 0:
        return
    for i,v in enumerate(g):
        yield v # /0
        if i > n-2: # start from zero, stop at *previous iteration*
            return

def fib_generator(): #f_{i} = f_{i-1} + f_{i-2}
    """Retorna o gerador com os números da sequência de Fibonacci.
    """
    i = 0
    while True:
        if i == 0:
            yield 1
            ultimo =1
            i += 1
            
            
        if i <= 1:
            yield 1
            ultimo = 1
            penultimo = 1
            i += 1
        
        else:
            yield ultimo + penultimo
            ultimo, penultimo = ultimo + penultimo, ultimo
            i += 1

def gen_fib_com (d):
    """Retorna o gerador de números de Fibonacci com exatamente d dígitos.
    """
    primeira_vez = True
    if primeira_vez:
        ultimo = next(fib_generator())
        if len(str(ultimo)) == d:
            yield ultimo
            primeira_vez = False
        primeira_vez = False
    
    while len(str(ultimo)) == d:
        ultimo, penultimo = next(fib_generator()), ultimo
        yield penultimo
    return



### Fatoração e Primalidade
cache_primos = {}

def multiplos (num):
    """Recebe o inteiro num e retorna uma tupla com os múltiplos de num (incluindo o proprio num).
    """
    lista = [x for x in range (1,int(num/2+1)) if num % x == 0]
    lista.append(num)
    return tuple(lista)

def crivo (n):
    """Retorna o conjunto de primos até n, utilizando o método do Crivo de Erastótenes.
    Ressalta-se que n representa o intervalo semiaberto [0,n[.
                                                             
    >>> crivo_bool (10)
    {2, 3, 5, 7}
    >>> crivo_bool (7)
    {2, 3, 5}
    """
    assert (isinstance(n, int)), "Para que a função funcione, n deve ser inteiro."
    #1. cria lista de tamanho n, com elementos True
    #2. caso base para evitar divisão por 0 e porque divisão por 1 não é critério para verificação de primos
    #3. percorremos a lista
    #3.1. se L[i] == True
    #3.2. seus múltiplos (a partir de i**2) viram False
    #4. retorna o conjunto de primos
    
    primos = set({})
    #1.
    L = [True for x in range (n)]
    #2.
    L[0], L[1] = False, False
    #3.
    for i in range (sqrt(n) +1):
        #3.1
        if L[i] == True:
            primos.add(i)
            for j in range (i**2, len(L), i):
                if j % i == 0:
                    L[j] = False
    return primos

def eh_primo (p):
    """Verifica se p é primo. Retorna True se for primo e False se não for.
    >>> eh_primo(10)
    False
    >>> eh_primo (5)
    True
    """
    assert (isinstance(p, int)), "A entrada de p deve ser um número inteiro"

    if p in cache_primos:    
        return cache_primos[p]
    
    #0. condições básicas para n não ser primo
    casos_base = {1,2,3} #O 3 fica inserido nos casos base devido à forma que o programa foi escrito: se p == 3, em 1., o range é nulo.
    if p in casos_base:
        return True
    if p % 2 == 0: # Pode nos poupar bastante tempo de cálculo.
        return False
    
    #1. criar uma lista com os inteiros menores que raiz de p
    N = [2*x-1 for x in range (2, int((p+1)/2))] #2*x-1 pois os pares já foram descartados em 0.
    
    #2. verificar se algum dos números da lista divide p
    for num in N:
        #3.1. caso sim, retornar False
        if p % num == 0:
            cache_primos[p] = False
            return False
    #3.2. caso não, retornar True
    cache_primos[p] = True
    return True

def primo_maior_que (n):
    """"Retorna o primeiro primo estritamente maior que n.
    >>> primo_maior_que(10)
    11
    >>> primo_maior_que(5)
    7
    """
    n += 1 # testar n não é o objetivo da função.
    if not eh_primo (n):
        return primo_maior_que(n)
    else:
        return n


### Combinação (Triângulo de Pascal)
cache_elemento = {}
def pascal_elemento (i, j):
    """Retorna o elemento do Triângulo de Pascal (combinação) de "coordenadas" (i,j), lembrando que a contagem começa em 0!
    """
    assert (i >= 0 or j >= 0 or j <= i), "Esse elemento não existe!"
    
    if (i,j) in cache_elemento:
        return cache_elemento[(i,j)]
    
    if i == j or j == 0: # estabelecemos os caso base
        return 1
    
    else: # e a recorrência
        result = pascal_elemento(i-1,j) + pascal_elemento (i-1,j-1)
        cache_elemento[(i,j)] = result
        return result

def pascal (L):
    """Retorna uma lista com o Triângulo de Pascal com L linhas. Cada linha é uma sub-lista.
    
    >>> pascal(3)
    [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
    """
    assert (L >= 0), "O número de linhas deve ser maior ou igual a zero!"

    L += 1 # para a contagem das linhas partir de 0
    A = [[x] for x in range (L)] #construímos as linhas, sem prestar atenção nos valores

    # e as colunas -1
    return [[pascal_elemento(i,j) for j in range(A[i][0]+1)] for i in range (L)]





class memoize:
	
	def __init__(self, func):
		self.func = func
		self.cache = {}
	
	def __call__(self, *args):
		if args in self.cache:
			return self.cache[args]
		else:
			val = self.func(*args)
			self.cache[args] = val
			return val
