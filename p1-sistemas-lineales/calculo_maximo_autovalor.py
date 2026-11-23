import numpy as np

"""
* A matriz cuadrada de la cual queremos hallar el máximo autovalor
* 
"""

def potencia_iterada(A, q, error_max, max_it):
    e = error_max + 1 # Para que entre en el bucle...
    cnt = 0
    beta = 0

    while e >= error_max and cnt < max_it:
        q_anterior = np.copy(q)
        x = np.dot(A, q)
        # np.abs pone cada valor del vector en positivo
        # np.argmax devuelve el índice del mayor valor
        # Se obtieve el valor al evaluar el índice en el vector
        beta = x[(np.argmax(np.abs(x)))]
        # Normalizamos en torno al mayor valor
        # Objetivo: evitar que los números exploten hacia el infinito
        q = x / beta
        e = (np.linalg.norm(q - q_anterior)) / np.linalg.norm(q) # Cambio con respecto el vector anterior
        cnt += 1

    return beta, q, cnt
