import numpy as np
import matplotlib.pyplot as plt
from sistemas_lineales import factolu_tridiagonal, resollu_tridiagonal


"""
* Calcula el ancho de los trozos
"""
def _calcular_h(x):
    n = x.shape[0] - 1
    h = np.zeros(n, dtype=float)
    for i in range(n):
        h[i] = x[i+1] - x[i]
    return h


"""
* Calcular los coeficientes del spline
"""
def coeficientes_spline(x, w, c0, cn):
    # Índice del último punto
    # 10 puntos - 1 = 9 (x0 - x9)
    n = x.shape[0] - 1 
    h = _calcular_h(x)
    # 8 incógnitas de los ci interiores
    m = n - 1   # número de incógnitas c1, ..., c_n-1
    
    
    alfa = np.zeros(m, dtype=float)   # diagonal inferior
    betta = np.zeros(m, dtype=float)  # diagonal principal
    gamma = np.zeros(m, dtype=float)  # diagonal superior
    b = np.zeros(m, dtype=float)

    
    # i = 1,2,...,8
    for i in range(1, n):
        # La ecuación i del spline ocupa la fila r = i-1 del sistema (índices empiezan en 0)
        r = i - 1
        betta[r] = 2 * (h[i-1] + h[i]) # Coeficiente ci
        if r > 0:
            alfa[r-1] = h[i-1]        # coeficiente de c_i-1
        if r < m - 1:
            gamma[r] = h[i]           # coeficiente de c_i+1
            
        b[r] = 6 * (w[i+1] - w[i]) / h[i] - 6 * (w[i] - w[i-1]) / h[i-1]

    # Condiciones adicionales
    b[0] -= h[0] * c0
    b[m-1] -= h[n-1] * cn

    factolu_tridiagonal(alfa, betta, gamma)
    c_interior = resollu_tridiagonal(alfa, betta, gamma, b)

    c = np.zeros(n + 1, dtype=float)
    c[0] = c0
    c[1:n] = c_interior
    c[n] = cn
    return c


"""
* Deducir en que trozo cae t
"""
def localizar_intervalo(x, t):
    n = x.shape[0] - 1
    if t <= x[0]:
        return 0
    if t >= x[n]:
        return n - 1
    izq, der = 0, n
    # Búsqueda binaria
    while der - izq > 1:
        medio = (izq + der) // 2
        if x[medio] <= t:
            izq = medio
        else:
            der = medio
    return izq


"""
* Evalúa el tramo s_i en el punto t
"""
def _tramo(x, w, c, h, i, t):
    return (c[i]   * (x[i+1] - t)**3 / (6*h[i])
          + c[i+1] * (t - x[i])**3   / (6*h[i])
          + (w[i]/h[i]   - c[i]*h[i]/6)   * (x[i+1] - t)
          + (w[i+1]/h[i] - c[i+1]*h[i]/6) * (t - x[i]))



def _tramo_derivada(x, w, c, h, i, t):
    return (- c[i]   * (x[i+1] - t)**2 / (2*h[i])
            + c[i+1] * (t - x[i])**2   / (2*h[i])
            - (w[i]/h[i]   - c[i]*h[i]/6)
            + (w[i+1]/h[i] - c[i+1]*h[i]/6))

def _tramo_derivada2(x, c, h, i, t):
    return c[i] * (x[i+1] - t) / h[i] + c[i+1] * (t - x[i]) / h[i]


"""
*Evalúa S, S' y S'' en todos los puntos del vector t
"""
def evaluar_spline(x, w, c, t):
    h = _calcular_h(x)
    S = np.zeros(t.shape[0], dtype=float)
    dS = np.zeros(t.shape[0], dtype=float)
    d2S = np.zeros(t.shape[0], dtype=float)
    for k in range(t.shape[0]):
        i = localizar_intervalo(x, t[k])
        S[k] = _tramo(x, w, c, h, i, t[k])
        dS[k] = _tramo_derivada(x, w, c, h, i, t[k])
        d2S[k] = _tramo_derivada2(x, c, h, i, t[k])
    return S, dS, d2S


def comprobar_spline(x, w, c):
    n = x.shape[0] - 1
    h = _calcular_h(x)
    err_interp = 0.0 # Mayor error de interpolación
    salto_d1 = 0.0 # Mayor error de pendiente
    salto_d2 = 0.0 # Mayor error de curvatura
    for i in range(n):
        # Ver si la curva paso por los puntos evaluando cada trozo en los dos extremos y comparando con el valor que debería de dar.
        err_interp = max(err_interp, abs(_tramo(x, w, c, h, i, x[i]) - w[i]), #extremo izquierdo
                        abs(_tramo(x, w, c, h, i, x[i+1]) - w[i+1])) #extremo derecho
    
    # Continuidad de la pendiente y de la curvatura
    for i in range(1, n):
        salto_d1 = max(salto_d1, abs(_tramo_derivada(x, w, c, h, i-1, x[i]) - _tramo_derivada(x, w, c, h, i, x[i])))
        salto_d2 = max(salto_d2, abs(_tramo_derivada2(x, c, h, i-1, x[i]) - _tramo_derivada2(x, c, h, i, x[i])))

    print("--- RESULTADOS (SPLINE CÚBICO) ---")
    print("Coeficientes ci = S''(x_i):")
    for i in range(n + 1):
        print(f"  c_{i} = {c[i]: .10f}")
    print(f"Máx. error de interpolación |S(x_i) - w_i|:   {err_interp:.3e}")
    print(f"Máx. salto de S'  en nodos interiores:        {salto_d1:.3e}")
    print(f"Máx. salto de S'' en nodos interiores:        {salto_d2:.3e}")
    print(f"S''(x_0) = {_tramo_derivada2(x, c, h, 0, x[0]):.6f}   S''(x_n) = {_tramo_derivada2(x, c, h, n-1, x[n]):.6f}")


def representar_spline(x, w, c, puntos=1000):
    t = np.linspace(x[0], x[-1], puntos)
    S, _, d2S = evaluar_spline(x, w, c, t)

    # En la misma columna dos gráficas
    # Las dos gráficas compartene el eje x
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
    # Coordenadas de los puntos x e y, linea contínua azul, grosor de la linea 2 (linewidth)
    ax1.plot(t, S, "-b", lw=2, label="Spline cúbico S(x)")
    # Dibujar los puntos en rojo
    ax1.plot(x, w, "ro", label="Puntos a interpolar")
    ax1.set_title("Ejercicio 1: spline cúbico")
    ax1.set_ylabel("y")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # S'' es lineal a trozos y pasa por (x_i, c_i): permite ver las condiciones en los extremos
    ax2.plot(t, d2S, "-g", lw=1.5, label="S''(x)")
    # ms (markersize): tamaño de los círculos
    ax2.plot(x, c, "ko", ms=4, label="c_i = S''(x_i)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("S''")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    # Ajusta los márgenes para que títulos y etiquetas no se monten unos sobre otros
    plt.tight_layout()
    plt.show()
