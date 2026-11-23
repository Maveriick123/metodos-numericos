import numpy as np


# La diagonal de L son todo 1s
def _descenso_unitario(A, B, x):
    n = x.shape[0]

    for i in range(n):
        s=0
        for j in range(i):
            s += A[i][j] * x[j]
        x[i] = B[i] - s

def _remonte(A, B, x):
    n = x.shape[0]

    for i in range(n-1,-1,-1):
        s=0
        for j in range(i+1,n):
            s+=A[i][j] * x[j]
        x[i] = (B[i] - s)/A[i][i]

    


"""
* A = LU
* Ax = b
* (L*U)*x = b
* Ly = b
* Ux = y
"""

def resollu(A, B):
    n = A.shape[0]

    x = np.zeros(n, "float")
    y = np.zeros(n, "float")

    # L*x = b
    _descenso_unitario(A, B, y)
    # U*x = y
    _remonte(A, y, x)
    return x


def _descenso(A, B, x):
    n = x.shape[0]

    for i in range(n):
        s=0
        for j in range(i):
            s += A[i][j] * x[j]
        x[i] = (B[i] - s) / A[i][i]

# No tenemos L' pero como A es simétrica, accederemos a sus simétricos
def _remonte_cholesky(A,B,x):
    n = x.shape[0]

    for i in range(n-1,-1,-1):
        s=0
        for j in range(i+1,n):
            s += A[j][i]* x[j]
        x[i] = (B[i] - s) / A[i][i]


"""
* A = LU
* Ax = b
* (L*L')*x = b
* Ly = b
* L'x = y
"""

def resolcholesky(A, B):
    n = A.shape[0]

    x = np.zeros(n, "float")
    y = np.zeros(n, "float")

    # L*x = b
    _descenso(A, B, y)
    # U*x = y
    _remonte_cholesky(A, y, x)
    return x


# alfa = [a21, a32, a43, ...]
def _descenso_unitario_tridiagonal(alfa, B, x):
    n = x.shape[0]
    # x[0] inmediato
    x[0] = B[0]
    # Entonces empezamos por i+1 por lo que el bucle va hasta n-1
    for i in range(n-1):
        x[i+1] = B[i+1] - (alfa[i]*x[i])

#betta = [a11,a22,a33,a44,...]
#gamma = [a12,a23,a34,(0),...]
def _remonte_tridiagonal(betta, gamma, B, x):
    n = x.shape[0]
    x[n-1] = B[n-1]/betta[n-1]
    for i in range(n-2, -1, -1):
        x[i] = (B[i] - gamma[i]*x[i+1] )/betta[i]


def resollu_tridiagonal(alfa, betta, gamma, B):
    n = betta.shape[0]
    x = np.zeros(n, "float")
    y = np.zeros(n, "float")

    _descenso_unitario_tridiagonal(alfa,B,y)
    _remonte_tridiagonal(betta,gamma, y, x)
    return x








