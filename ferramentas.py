# coding at utf-8

# Sessão de importações
import numpy as np
import matplotlib.pyplot as plt

### Bisseção
### --------
def passo_da_bissecao(f, a: float, b: float):
    """Retorna o novo intervalo após uma etapa da bisseção da função f,
    da forma (a,m) ou (m,b) segundo em qual seja possível garantir uma raiz de f.
    """
    m = (a + b) / 2
    if f(m) * f(a) < 0:
        return a, m
    else:
        return m, b


def bissecao(f, a: float, b: float, xtol=1e-8, ytol=1e-8, verbose=False):
    """Encontra uma raíz de  f  no intervalo  [a,b] pelo método da bisseção.

    Parâmetros
    ----------
    f : function
        Função a ser utilizada.
    a  : float
        Extremidade esquerda do intervalo em que será procurada uma raiz.
    b  : float
        Extremidade direita do intervalo em que será procurada uma raiz.
    xtol  : int/float, opcional
        Tolerância ao redor da raiz no eixo x. O padrão é 1e-8.
    ytol  : int/float, opcional
        Tolerância ao redor da raiz no eixo y. O padrão é 1e-8.
    verbose  : bool, opcional
        Se True, retorna como terceiro valor uma lista com as extremidades dos intervalos construídos da forma: [(a_1,b_1), (a_2,b_2), ...]

    Retorno
    -------
    Se verbose=False: retorna a tupla da forma (<raiz>, <numero_de_bissecoes>)
    se verbose=True:  retorna a tupla da forma (<raiz>, <numero_de_bissecoes>, [(a_1,b_1), (a_2,b_2), ...])
    """
    a0, b0 = a, b
    intervalos = [(a, b)]
    num_bissecoes = 0
    achei = False
    while not abs(b - a) < xtol and not abs(f((a + b) / 2)) <= ytol:  # Para que a função saia do laço, será necessário que sejam satisfeitos pelo menos um dos critérios de parada!
        # Verificamos se as extremidades do intervalo são raiz
        if f(a) == 0:
            valor_final, achei = a, True
            break
        elif f(b) == 0:
            valor_final, achei = b, True
            break

        # Fazemos uma bicessão
        a, b = passo_da_bissecao(f, a, b)
        num_bissecoes += 1  # Atualizamos o número de vezes que foram feitas bicessões
        if verbose:
            intervalos.append((a, b))
    # Se chegamos até aqui, é porque já podemos parar!
    if not achei:
        valor_final = (a + b) / 2
    if abs(f(valor_final)) > 1:  # Fazemos a prova real com uma tolerância muito grande porque a bisseção sempre encontra algum valor porque o intervalo fica pequeno o suficiente para passar na xtol. Dessa forma, avisamos ao usuário que o número obtido não se trata de uma raiz.
        # raise ValueError(f'Não foi possível encontrar uma raiz de {f} no intervalo [{a0}, {b0}].')
        print(f'Não foi possível encontrar uma raiz de {f} no intervalo [{a0}, {b0}].')
        valor_final = None
    if verbose:
        intervalos.append((a, b))
        return valor_final, num_bissecoes, intervalos
    else:
        return valor_final, num_bissecoes


def inv(f, a=0, b=1, xtol=1e-8, ytol=1e-8):
    """Retorna a função inversa de  f  no intervalo [a,b].
    A função inversa é garantida apenas para valores de  y  entre  f(a) e f(b)."""

    def func(y):
        def aux(x):
            return f(x) - y

        r, _ = bissecao(aux, a, b, xtol, ytol)
        return r

    return func


def bissect_geq(l, v: float) -> int:
    """First index  k  on an increasing list  l  such that  l[k] >= v.
    Returns  len(l)  if  l[-1] < v."""
    assert len(l) != 0, "A lista não pode ser indexada."
    if l[-1] < v: return len(l)  # "caso base"
    if l[0] >= v: return 0  # problema na verificação do l[a-1], pois acaba com a ordem da verificação.

    a, b = 0, len(l)

    while True:
        meio = (a + b) // 2
        v_meio = l[meio]
        if v_meio > v:  # Indica que o alvo está na primeira metade da lista.
            if l[a - 1] < v and l[a] >= v: return a  # Verificamos as extremidades do intervalo
            if l[b - 1] < v and l[b] >= v: return b
            b, meio = meio, (a + meio) // 2
        elif v_meio <= v:  # Indica que o alvo está na segunda metade da lista.
            if l[a - 1] < v and l[a] >= v: return a
            if l[b - 1] < v and l[b] >= v: return b
            a, meio = meio, (meio + b) // 2

            
### Método de Newton
### ----------------
def newton(f, df, x0: float=0, prec: float=1e-8, ytol: float=1e-8, maxiter: int=100, verbose: bool=False):
    """Aplica o método de Newton na função  f  e retorna a aprox. da raiz (com o erro mínimo erro_min).

    Parameters
    ----------
    f : function
        Função a qual será aplicada o Método de Newton
    df : function
        Derivada de f.
    x0 : float, opcional
        Ponto inicial a ser vasculhado. Idealmente, está próximo da raiz. O padrão é 0.
    prec : float, optional
        Tamanho do passo de newton pequeno o suficiente para retornarmos um valor. O padrão é 1e-8.
    ytol : float, optional
        Tamanho da tolerância ao redor do eixo y para retornarmos um valor. O padrão é 1e-8.
    maxiter : int, optional
        Máximo de iterações da função. O padrão é 100.
    verbose : bool, optional
        Estabelece se irá retornar, também, uma lista com os x_n alcansados.

    Returns
    -------
        Se verbose=True:
        <raíz: float>, <número de iterações: int>, <[x_1, x_2, x_3, ...]: list>
        Se verbose=False:
        <raíz: float>, <número de iterações: int>
    """
    trace = [x0]
    num_iter = 0
    x_i = x0

    while num_iter <= maxiter:
        passo = f(x_i)/df(x_i)
        novo_x, num_iter = x_i - passo, num_iter + 1
        trace.append(novo_x)
        x_i = novo_x
        if   abs(passo)  < prec: break
        elif abs(f(x_i)) < ytol: break
        

    if num_iter > maxiter:
        novo_x = None # Retornamos None para alertar o usuário que não encontramos uma raiz
    if verbose: return novo_x, num_iter, np.array(trace)
    else: return novo_x, num_iter


### Derivada
### --------

def df(f, x: float, h: float=1e-10):
    """Retorna a derivada numérica de  f  no ponto  x, com aproximação de  h.
    
    Parameters
    ----------
    f : function
        Função a ser derivada em  x.
    x : float
        Ponto em que  f  será derivada.
    h : float, optional
        Equivalente ao dh da derivada. Não utilize h <= 1e-16. O padrão é 1e-10.
    
    Returns
    -------
    p: float
        p é o valor da derivada numérica f'(x).
    """
    return (f(x+h) - f(x)) / h


def df_central(f, x: float, h: float=1e-10):
    """Retorna a derivada numérica central de  f  no ponto  x, com aproximação de  h.
    
    Parameters
    ----------
    f : function
        Função a ser derivada em  x.
    x : float
        Ponto em que  f  será derivada.
    h : float, optional
        Equivalente ao dh da derivada. Não utilize h <= 1e-16. O padrão é 1e-10.
    
    Returns
    -------
    p: float
        p é o valor da derivada numérica central f'(x).
    """
    return (f(x+h) - f(x-h)) / 2*h


def secante(f, a, b, xtol=1e-8, maxiter=100):
    """ Método da secante para a função  f  no intervalo  [a,b].

        Retorna um número  z  e as listas de extremidades esquerda e direita produzidas ao longo do algoritmo,
        que para quando o último passo é menor do que  xtol, ou depois de  maxiter  iterações.
    """
    def passo_secante(f, a, b): 
        """Dada a função  f, e o intervalo [a, b], aplica um passo do método da secante."""
        fa, fb = f(a), f(b) # Declaração de variaveis auxiliares
        return (a*fb - b*fa)/(fb - fa)
    
    # Estrutura recursiva
    def aux(f, a, b, xtol, num_iter, l, r):
        z = passo_secante(f, a, b) # Fazemos o passo
        num_iter += 1 # Atualizamos o número de iterações
        
        l.append(a)
        r.append(b)
        
        if abs(z - b) < xtol or num_iter == maxiter: return z, l, r # Atende aos critérios de parada
        else: return aux(f, b, z, xtol, num_iter, l, r)

    z, l, r = aux(f,a,b, xtol, 0, [], [])
    return z, np.array(l), np.array(r)


### Integral
### --------

def int_cauchy (f, a: float, b: float, N: float=1e4):
    """Retorna a integral definida de uma função vetorizada  f.
    
    Parameters
    ----------
    f : function
        Função a ser integrada;
    a : float
        Inicio do intervalo em que a integral será apreciada;
    b : float
        Final do intervalo em que a integral será apreciada;
    N : float, optional
        Número de subintervalos. O padrão é 1e4.
    
    Returns
    -------
    x : float
        Valor da integral em [a, b].
    """
    assert N > 0
    l, h = np.linspace(a, b, num=N, endpoint=False, retstep=True) # endpoint faz com que gere todos os x_k de x_0 até x_N-1
    return np.sum(f(l)) * h # np.sum  é mais rápido que  sum  pois é mais específico (otimizado)

def int_trap (f, a: float, b: float, N: int=1e4) -> float:
    """Retorna a integral definida de uma função vetorizada  f.
    
    Parameters
    ----------
    f : function
        Função a ser integrada;
    a : float
        Inicio do intervalo em que a integral será apreciada;
    b : float
        Final do intervalo em que a integral será apreciada;
    N : int, optional
        Número de retângulos. O padrão é 1e4.
    
    Returns
    -------
    x : float
        Valor da integral em [a, b].
    """
    assert N > 0
    l, h = np.linspace(a, b, num=N, endpoint=False, retstep=True)
    return np.sum(f(l)) * h + (f(b) - f(a)) * h/2

def int_midp (f, a: float, b: float, N: int=1e4) -> float:
    """Retorna a integral definida de uma função vetorizada  f no intervalo  [a,b] com N retângulos centrados nos pontos médios.
    
    Parameters
    ----------
    f : function
        Função a ser integrada;
    a : float
        Inicio do intervalo em que a integral será apreciada;
    b : float
        Final do intervalo em que a integral será apreciada;
    N : int, optional
        Número de retângulos. O padrão é 1e4.
    
    Returns
    -------
    x : float
        Valor da integral em [a, b].
    """
    assert N > 0
    l, h = np.linspace(a, b, num=N, endpoint=False, retstep=True)
    mids = l + h/2
    return np.sum(f(mids)) * h

def int_simpson (f, a: float, b: float, N: int=1e4) -> float:
    """Retorna a integral definida de uma função vetorizada  f no intervalo  [a,b]  com N > 0 
    subintervalos.
    
    Parameters
    ----------
    f : function
        Função a ser integrada;
    a : float
        Inicio do intervalo em que a integral será apreciada;
    b : float
        Final do intervalo em que a integral será apreciada;
    N : int, optional
        Número de subintervalos. O padrão é 1e4.
    
    Returns
    -------
    x : float
        Valor da integral em [a, b].
    """
    assert N > 0
    l, h = np.linspace(a,b, num=N, endpoint=False, retstep=True)
    mids = l + h/2
    return ( 4*np.sum(f(mids)) + 2*np.sum(f(l)) + (f(b) - f(a)) ) * h/6


# Regressão
# ---------
def reg_poly(xs, ys, grau):
    """Retorna a função da regressão polinomial dos pontos (xs,ys).
    """
    vander = np.vander(xs, grau+1) 
    coefs, *_ = np.linalg.lstsq(vander, ys, rcond=None)
    p = np.poly1d(coefs) 
    return p 

def regress_with_error(xs, ws, phis):
    """Regressão linear dos pontos  (xs,ys)  para a base de funções dada pela lista  phis,
    retornando os coeficientes e o erro da regressão."""
    M_list = []
    for x in xs:
        linha = []
        for phi in phis:
            linha.append( phi(x) )
        M_list.append(linha)
    M = np.asmatrix(M_list)
    coefs, err, *_ = np.linalg.lstsq(M, ws, rcond=None)
    return coefs, err

def reconstruct(coefs, base):
    """Retorna a função correspondente aos coeficientes e à base escolhida de uma regressão.
    """
    def m(x):   
        ans = 0
        for beta, coef in zip(base, coefs):
            ans += coef * beta(x)
        return ans         
        
    return m

### Gráficos
### --------

def graph_erro_num_subintervalos (methods: list, f,  ans: float, a: float, b: float, ns):
    """Plota o gráfico do erro das funções em  methods  , que utilizam o intervalo  [a,b]  aplicados em  f  com  ns retângulos.
    
    Ex.: methods = [int_r, int_t, int_midp]
         f = np.cos
         ns = np.logspace(2,6, num=50, dtype=int)
         
    """
    for m in methods:
        err = [m(f, a, b, n) - ans for n in ns]
        plt.loglog(ns, np.abs(err), label=m.__name__)
    plt.legend(title='Método')
    plt.xlabel(f'# subdivisões do intervalo [{a},{b}]')
    plt.ylabel('Erro de integração em função do número de subintervalos')
    plt.grid
    
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
