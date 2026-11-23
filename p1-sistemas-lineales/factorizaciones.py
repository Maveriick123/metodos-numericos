import numpy as np

"""
* Se asume que la matriz A es cuadrada.
* Los coeficientes L y U se almacenan en la matriz A.
* Es importante el orden de los bucles, ya que para calcular los coeficientes de L necesitamos los elementos de la diagonal principal pertenecientes a U(...)
"""
# Forma Doolitle (...)
def factolu(A):
    # shape devuelve una tupla (filas, columnas), al ser una matriz cuadrada podemos coger cualquiera
    n = A.shape[1] 
    for j in range(n):
        # Cálculo de los coeficientes de U 
        # Saltamos la primera fila puesto que sería redundante A[0][j] = A[0][j]
        for i in range(1, j+1): # Recorremos la triangular superior de A
            s = 0
            for k in range(i):
                s += A[i][k] * A[k][j]
                # --> L[i][k](misma fila) * U[k][u](misma columna)
            A[i][j] = A[i][j] - s
        # Cálculo de los coeficientes de L
        for i in range(j+1, n): # Recorremos la triangular estrictamente inferior de A
            s = 0
            for k in range(j):
                s += A[i][k] * A[k][j]
                # --> L[i][k](misma fila) * U[k][u](misma columna)
            A[i][j] = (A[i][j] - s) / A[j][j]

"""
* Al ser una matriz simétrica llega con calcular la triangular inferior.
* Se asume que es una matriz simétrica y definida positiva.
"""

def factoCholesky(A):

    n = A.shape[0]

    for j in range(n):
        # Parte superior de la matriz
        # En A[0][0] nunca tiene que restar nada en la raíz

        # Calculo de la diagonal
        s = 0
        for k in range (j):
            s+= A[j][k] **2
        
        A[j][j] = np.sqrt(A[j][j]-s) 

        # Se necesita la diagonal para calcular la matriz triangular superior
        for i in range(j + 1 , n):
            s = 0
            for k in range(j):
                # s += A[i][k] * A[k][j]
                # ---------------> La parte superior no esta calculada, entonces necesito su simétrico
                s += A[i][k] * A[j][k]
            A[i][j] = (A[i][j] - s)/A[j][j]


"""
* Todas las listas tienen la misma longitud.
* Las listas que no se correspondan con la diagonal principal llevarán un cero en el último elemento.
* @alfa: se corresponde con la diagonal inferior.
* @betta: se corresponde con la diagonal principal.
* @gamme: se corresponde con la diagonal superior.
"""                
def factolu_tridiagonal(alfa, betta, gamma):
    n = alfa.shape[0]
    # gamma queda igual (...)
    # Cálculo de la diagonal principal
    # a[0][0] que se queda igual

    # alfa[0] = alfa[0]/betta[0]

    # El último elemento de alfa es un cero por lo que no hay nada que calcular.
    # De esta forma hacemos que el bucle recorra hasta la penúltima posición
    # Por ende calculamos el último elemento de betta fuera

    for i in range (1, n):
        alfa[i-1] = alfa[i-1] / betta[i-1]
        betta[i] = betta[i] - alfa[i-1] * gamma[i-1] 









