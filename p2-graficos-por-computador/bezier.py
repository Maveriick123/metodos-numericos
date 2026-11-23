import numpy as np
import matplotlib.pyplot as plt
from math import factorial
from sistemas_lineales import factolu, resollu


# =============================================================
#  2(a): ALGORITMO DE DE CASTELJAU
# =============================================================

"""
* Algoritmo 4 (De Casteljau), página 46 apuntes.
* @c: puntos de control c_0, ..., c_n (una fila por punto, de cualquier dimensión d)
* Devuelve el punto p(t) de la curva de Bézier.
"""
def de_casteljau(c, t):
    n = c.shape[0] - 1
    p = c.copy()                 # copia para no modificar los puntos de control, crítico
    for m in range(1, n + 1):    
        for k in range(n - m + 1):   
            p[k] = (1 - t) * p[k] + t * p[k+1]
    return p[0]              


"""
* Evalúa la curva en valores de t equiespaciados en [0, 1].
* Devuelve una matriz con un punto de la curva por fila.
"""
def curva_bezier(c, puntos=1000):
    t = np.linspace(0, 1, puntos)
    curva = np.zeros((puntos, c.shape[1]), dtype=float)
    for j in range(puntos):
        curva[j] = de_casteljau(c, t[j])
    return curva


def representar_bezier(c, curva, titulo):
    plt.figure(figsize=(8, 7))
    # k color negro o circulo en cada punto unidos por ---
    # linewidth
    # markersize
    # c[:,0] las x
    # c[:, 1] las y
    plt.plot(c[:, 0], c[:, 1], "ko--", lw=1, ms=5, label="Polígono de control")
    for k in range(c.shape[0]):
        # el texto entre $$ esta en formato latex
        # {{ == { y {k} == k
        # textcoords y xytext es decir para que el texto no se pinte encima del punto
        plt.annotate(f"$c_{{{k}}}$", (c[k, 0], c[k, 1]), textcoords="offset points", xytext=(5, 5))
    plt.plot(curva[:, 0], curva[:, 1], "-r", lw=2, label="Curva de Bézier")
    plt.title(titulo)
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


# =============================================================
#  2(b) y 2(c): VARIAS CURVAS Y CONEXIÓN DE CURVAS
# =============================================================

"""
* Divide los puntos de control en grupos según una lista de rangos de índices.
* Los rangos están en data.py
"""
def dividir_puntos(c, rangos):
    tramos = []
    for (ini, fin) in rangos:
        # fin + 1 para incluir el último punto
        tramos.append(c[ini:fin+1].copy())
    return tramos


# Sale de aquí:
"""
c_n = d_0                                   (se tocan: misma posición)
n (c_n - c_{n-1}) = m (d_1 - d_0)           (misma tangente: unión suave)
"""
def punto_union(c_penultimo, d_segundo, n, m):
    return m / (n + m) * d_segundo + n / (n + m) * c_penultimo


"""
* 2(c): se aplica la conexión en las tres uniones I -> II, II -> III y III -> I.
* Mínimas modificaciones: en cada unión solo se mueven los dos extremos que se
* tocan (pasan a ser el mismo punto c_n = d_0); el resto de puntos no cambia.
"""
def cerrar_curvas(tramos):
    tramos = [c.copy() for c in tramos]   # no se modifican los originales
    N = len(tramos)
    for j in range(N):
        X = tramos[j]
        # El módulo es para que la última curva se una con la primera.
        Y = tramos[(j + 1) % N]
        n = X.shape[0] - 1
        m = Y.shape[0] - 1
        q = punto_union(X[n-1], Y[1], n, m)
        X[n] = q      # c_n
        Y[0] = q      # d_0 = c_n
    return tramos


def representar_tramos(tramos, nombres, titulo, originales=None):
    colores = ["tab:red", "tab:green", "tab:blue", "tab:orange", "tab:purple"]
    plt.figure(figsize=(8, 7))
    if originales is not None:
        for c in originales:
            #o: (:) linea punteada
            plt.plot(c[:, 0], c[:, 1], "o:", color="gray", lw=1, ms=4, alpha=0.6)
        # Sólo se hace el plot vacío para mostrar la leyenda, (truco)
        plt.plot([], [], "o:", color="gray", label="Polígonos originales")
    for j in range(len(tramos)):
        c = tramos[j]
        # El módulo se usa por si hubiese más de 5 tramos que no hubiese falta de colores nunca
        # Así, es escalable
        # Se van repitiendo alternadamente
        color = colores[j % len(colores)]
        curva = curva_bezier(c)
        # El nuevo poligono de control
        plt.plot(c[:, 0], c[:, 1], "o--", color=color, lw=1, ms=5, alpha=0.6)
        # La curva asociada
        plt.plot(curva[:, 0], curva[:, 1], "-", color=color, lw=2.5, label=f"Curva {nombres[j]}")
    plt.title(titulo)
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


# =============================================================
#  2(d): CURVA DE BÉZIER RACIONAL
# =============================================================


# Algoritmo 5, página 52 apuntes
def de_casteljau_racional(c, w, t):
    n = c.shape[0] - 1
    p = c.copy()                         
    pesos = np.array(w, dtype=float)     
    for l in range(1, n + 1):
        for k in range(n - l + 1):
            w_nuevo = (1 - t) * pesos[k] + t * pesos[k+1]
            # se usan pesos[k] y pesos[k+1] del nivel anterior: pesos[k] se actualiza después
            p[k] = (1 - t) * pesos[k] / w_nuevo * p[k] + t * pesos[k+1] / w_nuevo * p[k+1]
            pesos[k] = w_nuevo
    return p[0]                          # r(t) = p_0^n


def curva_bezier_racional(c, w, puntos=1000):
    t = np.linspace(0, 1, puntos)
    curva = np.zeros((puntos, c.shape[1]), dtype=float)
    for j in range(puntos):
        curva[j] = de_casteljau_racional(c, w, t[j])
    return curva


def representar_racional(c, w, curva, indices, titulo):
    plt.figure(figsize=(8, 7))
    plt.plot(c[:, 0], c[:, 1], "ko--", lw=1, ms=5, label="Polígono de control")
    for k in range(c.shape[0]):
        # Se pone el índice original del punto (c_2, ..., c_11) y su peso
        plt.annotate(f"$c_{{{indices[k]}}}$ (w={w[k]:g})", (c[k, 0], c[k, 1]),
                        textcoords="offset points", xytext=(5, 5), fontsize=8)
    plt.plot(curva[:, 0], curva[:, 1], "-r", lw=2, label="Bézier racional")
    plt.title(titulo)
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()


# =============================================================
#  2(e): INTERPOLACIÓN CON CURVAS DE BÉZIER
# =============================================================

def matriz_interpolacion(n):
    M = np.zeros((n + 1, n + 1), dtype=float)
    for i in range(n + 1):
        for j in range(n + 1):
            # t_i = i/n (equiespaciados)
            # Sacado de los apuntes (página 49), ...
            # En Python 0**0 = 1 -> la fila 0 queda [1, 0, ..., 0] y la última [0, ..., 0, 1]
            # Es decir, si t0 = 0 obtenemos c0 = q0 y si tn = 1, cn = qn
            # (la curva empieza en el primer punto y acaba en el último)
            M[i][j] = factorial(n) * (n - i)**(n - j) * i**j / (factorial(j) * factorial(n - j) * n**n)
    return M


"""
* Se resuelve M c = q con la LU de la Práctica 1.
* M se factoriza una sola vez y se resuelve un sistema por coordenada (x, y, z).
* Devuelve los puntos de control c_0, ..., c_n.
"""
def interpolar_bezier(q):
    n = q.shape[0] - 1
    M = matriz_interpolacion(n)
    factolu(M)               # M queda sobrescrita con L y U
    c = np.zeros(q.shape, dtype=float)
    for d in range(q.shape[1]):
        c[:, d] = resollu(M, q[:, d])
    return c


def representar_interpolacion(q, c, titulo):
    # Con los puntos de control obtenidos se construye la curva con De Casteljau
    curva = curva_bezier(c)
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.plot(curva[:, 0], curva[:, 1], curva[:, 2], "-b", lw=2, label="Curva de Bézier interpolante")
    ax.scatter(q[:, 0], q[:, 1], q[:, 2], color="red", s=30, label="Puntos a interpolar $q_i$")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.set_title(titulo)
    ax.legend()
    plt.show()
