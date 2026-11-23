import numpy as np

"""
* Compara la solución obtenida con la de NumPy, calcula el error relativo, el residuo,
muestra el tiempo de CPU y guarda la solución en un archivo de texto.
"""



def comprobacion(A_original, B, x, cpu_time, flag):
    # -------> 1. Tiempo de ejecución
    print(f"--- RESULTADOS ---")
    print(f"Tiempo de CPU empleado: {cpu_time:.6f} segundos")
    # -------> 2. Comprobación de resultados
    s = np.linalg.solve(A_original, B)

    error_relativo = np.linalg.norm(x - s) / np.linalg.norm(s)
    print(f"Error relativo (respecto a numpy (||x - s / s||)): {error_relativo}")

    y_res =  np.dot(A_original, x) - B
    norma_residuo = np.linalg.norm(y_res)
    print(f"Magnitud del error(||A * x - B||): {np.linalg.norm(y_res)}")

    error_residuo_relativo = norma_residuo / np.linalg.norm(B)
    print(f"Error relativo del residuo (||Ax - b|| / ||b||): {error_residuo_relativo}")

    # -------> 3. Almacenamiento y impresión de resultados

    if(flag == 1): nombre_archivo= "soluciones_lu.txt"
    if(flag == 2): nombre_archivo= "soluciones_cholesky.txt"
    if(flag == 3): nombre_archivo= "soluciones_lu_tridiagonal.txt"
    if(flag == 4): nombre_archivo= "soluciones_seidel.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("Indice\tValor\n")
        for i, val in enumerate(x):
            f.write(f"{i}\t{val}\n")
    print(f"Vector solución guardado correctamente en '{nombre_archivo}'")
    
    print(f"Solución del sistema: {x}\n")

def comprobacion_pot_it(A, beta, q, cpu_time, nombre_archivo="soluciones_potencia.txt"):
    print(f"--- RESULTADOS (POTENCIA ITERADA) ---")
    print(f"Tiempo de CPU empleado: {cpu_time:.6f} segundos")
    print(f"Máximo autovalor encontrado ($beta$): {beta}")
    print(f"Autovector asociado ($q$): {q}\n")

    residuo = np.dot(A, q) - beta * q
    error_relativo = np.linalg.norm(residuo) / np.linalg.norm(beta * q)
    print(f"Error relativo de autovalor/autovector (||Aq - beta*q|| / ||beta*q||): {error_relativo}")
    print(f"Vector solución guardado correctamente en '{nombre_archivo}'")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"Autovalor maximo: {beta}\n")
        f.write("Indice\tComponente_Autovector\n")
        for i, val in enumerate(q):
            f.write(f"{i}\t{val}\n")
            
