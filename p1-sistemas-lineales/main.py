from factorizaciones import factolu, factoCholesky, factolu_tridiagonal
from resolución_sistemas import resollu, resolcholesky, resollu_tridiagonal
from func_auxiliares import comprobacion, comprobacion_pot_it
from metodos_iterativos import gauss_seidel
from calculo_maximo_autovalor import potencia_iterada
import data
import numpy as np
import time
import sys

"""
1 --> LU
2 --> CHOLESKY
3 --> TRIDIAGONAL
4 --> GAUSS-SEIDEL
5 --> POTENCIA ITERADA
"""

if len(sys.argv) > 1:
    SELECTION_FLAG = int(sys.argv[1])
else:
    SELECTION_FLAG = 1



def lu(A_mod):
    factolu(A_mod)
    x = resollu(A_mod, data.b_lu)
    return x

def cholesky(A_mod):
    factoCholesky(A_mod)
    x = resolcholesky(A_mod, data.b_cholesky)
    return x

def tridiagonal(alfa, betta, gamma):
    factolu_tridiagonal(alfa, betta, gamma)
    x = resollu_tridiagonal(alfa, betta, gamma, data.b_tridiagonal)
    return x

    



"""
* Para medir usamos el tiempo de CPU que consumo el proceso
* Así nos evitamos ruidos por interrupciones de otros procesos, es más fiable la medición
"""

if(SELECTION_FLAG == 1):
    A_mod = np.array(data.A_lu, dtype=float)

    init_time = time.process_time()
    x = lu(A_mod)
    end_time = time.process_time()
    total_cpu_time = end_time - init_time

    a_original = np.array(data.A_lu, dtype=float)
    comprobacion(a_original ,data.b_lu, x, total_cpu_time, SELECTION_FLAG)

elif(SELECTION_FLAG == 2):
    A_mod = np.array(data.A_cholesky, dtype=float)

    init_time = time.process_time()
    x = cholesky(A_mod)
    end_time = time.process_time()
    total_cpu_time = end_time - init_time

    a_original = np.array(data.A_cholesky, dtype=float)
    comprobacion(a_original ,data.b_cholesky, x, total_cpu_time, SELECTION_FLAG)

elif(SELECTION_FLAG == 3):
    alfa = np.array(data.alfa, dtype=float)
    betta = np.array(data.betta, dtype=float)
    gamma = np.array(data.gamma, dtype=float)

    init_time = time.process_time()
    x = tridiagonal(alfa, betta, gamma)
    end_time = time.process_time()
    total_cpu_time = end_time - init_time

    # Construimos la matriz para poder pasarsela al método de comprobación
    # El parámetro k toma como punto de referencia la diagonal principal
    # Al sumar punto a punto las tres matrices solo habra valores en los lugares donde se insertaron
    a_original = np.diag(data.betta) + np.diag(data.alfa[:-1], k=-1) + np.diag(data.gamma[:-1], k=1)

    comprobacion(a_original ,data.b_tridiagonal, x, total_cpu_time, SELECTION_FLAG)

elif(SELECTION_FLAG == 4):
    x = np.zeros(data.b_seidel.shape[0])
    max_it = 10000
    epsilon = 1e-15 

    init_time = time.process_time()
    # Como A nunca se modifica sólo se lee se pasa su puntero directamente
    it, x = gauss_seidel(x, max_it, epsilon, data.A_seidel, data.b_seidel)
    end_time = time.process_time()
    total_cpu_time = end_time - init_time

    print(f"Número de iteraciones: {it}")
    comprobacion(data.A_seidel, data.b_seidel, x, total_cpu_time, SELECTION_FLAG)

elif SELECTION_FLAG == 5:
    
    q_ini = np.ones(data.a_pi.shape[0])
    max_error = 1e-15
    max_iter = 10000

    init_time = time.process_time()
    beta, q, k = potencia_iterada(data.a_pi, q_ini, max_error, max_iter)
    end_time = time.process_time()
    total_cpu_time = end_time - init_time

    print(f"Número de iteraciones: {k}")
    comprobacion_pot_it(data.a_pi, beta, q, total_cpu_time, "soluciones_potencia.txt")