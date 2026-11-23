import numpy as np

"""
* Métodos directos de resolución de sistemas reutilizados de la Práctica 1.
* En esta práctica aparecen dos tipos de sistemas:
    - Tridiagonal: al calcular los coeficientes ci del spline cúbico.
    - Lleno: al interpolar con una curva de Bézier (2e).
"""


# =============================================================
#  SISTEMAS TRIDIAGONALES
# =============================================================

"""
* Todas las listas tienen la misma longitud n.
* @alfa:  diagonal inferior  -> alfa[i]  = a_{i+1, i}  (el último elemento no se usa)
* @betta: diagonal principal -> betta[i] = a_{i, i}
* @gamma: diagonal superior  -> gamma[i] = a_{i, i+1} (el último elemento no se usa)
* La factorización se guarda sobre los propios vectores:
"""
def factolu_tridiagonal(alfa, betta, gamma):
    n = betta.shape[0]
    for i in range(1, n):
        alfa[i-1] = alfa[i-1] / betta[i-1]
        betta[i] = betta[i] - alfa[i-1] * gamma[i-1]


def _descenso_unitario_tridiagonal(alfa, B, x):
    n = x.shape[0]
    x[0] = B[0]
    for i in range(n-1):
        x[i+1] = B[i+1] - alfa[i] * x[i]


def _remonte_tridiagonal(betta, gamma, B, x):
    n = x.shape[0]
    x[n-1] = B[n-1] / betta[n-1]
    for i in range(n-2, -1, -1):
        x[i] = (B[i] - gamma[i] * x[i+1]) / betta[i]


"""
* Requiere haber llamado antes a factolu_tridiagonal.
* A = LU  ->  Ly = b ; Ux = y
"""
def resollu_tridiagonal(alfa, betta, gamma, B):
    n = betta.shape[0]
    x = np.zeros(n, dtype=float)
    y = np.zeros(n, dtype=float)
    _descenso_unitario_tridiagonal(alfa, B, y)
    _remonte_tridiagonal(betta, gamma, y, x)
    return x


# =============================================================
#  SISTEMAS LLENOS: LU (sin pivotaje)
# =============================================================

"""
* Se asume que la matriz A es cuadrada.
* Los coeficientes de L (sin su diagonal de unos) y de U se almacenan sobre la propia A.
* Orden de los bucles: por columnas; para los coeficientes de L de la columna j
hace falta antes el elemento U[j][j] de esa misma columna.
"""
def factolu(A):
    n = A.shape[0]
    for j in range(n):
        # Coeficientes de U (triangular superior, columna j)
        for i in range(1, j+1):
            s = 0.0
            for k in range(i):
                s += A[i][k] * A[k][j]      # L[i][k] * U[k][j]
            A[i][j] = A[i][j] - s
        # Coeficientes de L (triangular estrictamente inferior, columna j)
        for i in range(j+1, n):
            s = 0.0
            for k in range(j):
                s += A[i][k] * A[k][j]      # L[i][k] * U[k][j]
            A[i][j] = (A[i][j] - s) / A[j][j]


# L*y = b  (diagonal de L formada por unos)
def _descenso_unitario(A, B, x):
    n = x.shape[0]
    for i in range(n):
        s = 0.0
        for j in range(i):
            s += A[i][j] * x[j]
        x[i] = B[i] - s


# U*x = y
def _remonte(A, B, x):
    n = x.shape[0]
    for i in range(n-1, -1, -1):
        s = 0.0
        for j in range(i+1, n):
            s += A[i][j] * x[j]
        x[i] = (B[i] - s) / A[i][i]


"""
* Requiere haber llamado antes a factolu(A).
* A = LU  ->  Ly = b ; Ux = y
* Como la factorización se hace una sola vez, se pueden resolver varios segundos miembros
* con la misma A (en el 2e: uno por cada coordenada x, y, z).
"""
def resollu(A, B):
    n = A.shape[0]
    x = np.zeros(n, dtype=float)
    y = np.zeros(n, dtype=float)
    _descenso_unitario(A, B, y)
    _remonte(A, y, x)
    return x
