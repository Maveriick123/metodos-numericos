import numpy as np

def gauss_seidel(x_ini, max_iter, epsilon, A, b):

    cnt = 0 # Contador de iteraciones
    n = A.shape[0] 
    error = epsilon + 1 # Siempre se entrará en el bucle...
    x = np.copy(x_ini)

    while (cnt < max_iter) and (error >= epsilon):
        x_ref = np.copy(x)
        
        for i in range(n):
            # Sumatorio con los valores de la iteración actual (ya actualizados)
            s1 = sum(A[i][j] * x[j] for j in range(i))
            # Sumatorio con los valores de la iteración anterior
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            
            x[i] = (b[i] - s1 - s2) / A[i][i]

        cnt += 1
        error = np.linalg.norm(x - x_ref) / np.linalg.norm(x)

    return cnt, x