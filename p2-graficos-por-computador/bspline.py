import numpy as np
import matplotlib.pyplot as plt


# =============================================================
#  EJERCICIO 3: B-SPLINE DE TERCER GRADO
# =============================================================

# p es el grado del spline, en este caso como es cúbico, 3
# n es el índice del último punto de ctrl
# Premisa 1: p <= n

# Los nodos interiores estan equiespaciados
# Página 56 de los apuntes

# En este caso son 17 puntos (n=16), p=3 y m=20 -> 21 nodos
#  u = [0 0 0 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 14 14 14]

def nodos_uniforme_abierto(n, p):
    m = n + p + 1 # Premisa 2
    u = np.zeros(m + 1, dtype=float)
    # Desde u0 hasta um
    # El conjunto de nodos contiene n + p + 2 nodos
    for k in range(m + 1):
        if k <= p:
            u[k] = 0
        elif k <= n:
            u[k] = k - p
        # si n < k <= n + p + 1
        else:
            u[k] = n + 1 - p
    return u

# Para localizar en que tramo está t
# Así se sabe que p + 1 puntos de control usar
def buscar_k(u, t):
    m = u.shape[0] - 1
    for k in range(m):
        if u[k] <= t < u[k+1]:
            return k
    return m # t=14


"""
* Algoritmo 6 (de De Boor), pág. 59.
* Calcula el punto S(t) de la curva B-spline.
* @c: puntos de control (una fila por punto)
* @u: nodos
* @p: grado
"""

# p = 3 --> 3 rondas
# I.e: t = 2.5 --> k = 5
# Mezcla los 4 puntos de ctrl correspondientes de 2 en 2
def de_boor(c, u, p, t):
    n = c.shape[0] - 1 # n = 16
    k = buscar_k(u, t)
    
    if k >= n + 1: # Fin de la curva, caso en el que k = m. Ver buscar_k()
        return c[n].copy() # Se devuelve c16
    
    d = np.zeros((p + 1, c.shape[1]), dtype=float)
    for j in range(p + 1): # Copiar los 4 puntos de ctrl del tramo
        d[j] = c[j + k - p] # 0 + 5 - 3 = c2, c3, c4, c5
    
    for r in range(1, p + 1): # tres rondas (p=3) --> r = 1,2,3
        for j in range(p, r - 1, -1): # (3, (0,1,2), -1), el step es -1, vamos hacia atrás
            # Hacia atrás para no machacar d[j-1] antes de usarlo
            # La ventana se va encojiendo en cada ronda
            # La ventana de cada mezcla es el intervalo en el que los puntos (ctrl) que se mezclan
            # están vivos a la vez. Cada c_i está vivo en [u_i, u_{i+p+1}) (con p=3, u_{i+4})
            # alfa reparte el peso de cada punto en función de lo avanzado que este t en el intervalo
            # (t - inicio) / (fin - inicio)
            alfa = (t - u[j+k-p]) / (u[j+1+k-r] - u[j+k-p])
            # Punto del segmento que une los dos puntos (izq y derecha)
            d[j] = (1 - alfa) * d[j-1] + alfa * d[j]
            
    # S(t)
    return d[p]


"""
* Evalúa la curva en valores de t equiespaciados.
* Dominio del parámetro t en [u_p, u_{n+1}); se incluye el extremo
* u_{n+1}, que De Boor resuelve con la rama k >= n+1 -> S(t) = c_n.
* Devuelve una matriz con un punto de la curva por fila.
"""
def curva_bspline(c, u, p, puntos=1000):
    n = c.shape[0] - 1 # n = 16 (índice del último, son 17 puntos)
    t = np.linspace(u[p], u[n+1], puntos) # Puntos equiespaciados
    # OBSERVACIÓN: incluimos u[n+1]
    curva = np.zeros((puntos, c.shape[1]), dtype=float)
    for j in range(puntos):
        curva[j] = de_boor(c, u, p, t[j])
    return curva


def representar_bspline(c, u, p, curva, titulo):
    print(f"Nodos uniformes abiertos (n = {c.shape[0]-1} >= p = {p}):")
    print(f"u = {u}")

    plt.figure(figsize=(8, 7))
    # Polígono de control: k color negro, o círculo en cada punto unidos por --
    # lw: linewidth
    # ms: markersize
    plt.plot(c[:, 0], c[:, 1], "ko--", lw=1, ms=5, label="Polígono de control")
    for k in range(c.shape[0]):
        # el texto entre $$ está en formato latex, fstring: {{{k}}} -> {k}
        # Las etiquetas se pintan 5 puntos tipográficos sobre c hacia arriba y hacia la derecha
        plt.annotate(f"$c_{{{k}}}$", (c[k, 0], c[k, 1]), textcoords="offset points", xytext=(5, 5))
    plt.plot(curva[:, 0], curva[:, 1], "-b", lw=2, label=f"B-spline de grado {p}")
    plt.title(titulo)
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
