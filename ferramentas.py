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

def bissecao (f, a, b, xtol=1e-8, visual:bool=False):
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

def newton (f, x_0, maxiter=1e3, erro_min=1e-16, visual:bool=False):
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
        if visual:
            x_n.append(x)
    if visual: return x, x_n
    else: return x



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