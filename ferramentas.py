# utf-8

def passo_da_bissecao (f, a, b):
    """Retorna o novo intervalo após uma etapa da bisseção da função f, 
    da forma (a,m) ou (m,b) segundo em qual seja possível garantir uma raiz de f.
    """
    m = (a+b)/2
    if f(m)*f(a) < 0:
        return a, m
    else:
        return m, b

def bissecao (f, a, b, xtol=1e-8, visual=False):
    """Encontra uma raíz de  f  no intervalo  [a,b].
    
    Se visual=True: Retorna a raiz e uma lista com as extremidades dos intervalos construídos da forma:
    (raíz, [(a_1,b_1), (a_2,b_2), ...])
    
    Se visual=False: Retorna a raíz de  f  no intervalo.
    """    
    intervalos = [(a,b)]
    while abs(b-a) >= xtol: # "invertemos" o teste de parada. agora é teste de continnuada...
        a, b = passo_da_bissecao (f, a, b)
        if visual:
            intervalos.append((a,b))
    # Se chegamos até aqui, é porque o intervalo está pequeno o suficiente!
    if visual:
        intervalos.append((a,b))
        return (a+b)/2, intervalos
    else:
        return (a+b)/2
    

def newton (f, df, x, xtol=1e-8):
    """Aplica o método de Newton na função f.
    """


def deriv (f):
    """Retorna a função derivada de f.
    """


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
    """ Retorna o gerador de números de Fibonacci com exatamente d dígitos.
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