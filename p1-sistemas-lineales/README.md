# Práctica 1 · Sistemas de ecuaciones lineales

Implementación en Python de métodos directos e iterativos para la resolución de sistemas de ecuaciones lineales y para el cálculo de autovalores. Todos los algoritmos están programados desde cero; NumPy solo se utiliza como estructura de datos y para validar los resultados.

## Métodos implementados

**Métodos directos**, con sus correspondientes algoritmos de descenso y remonte:
- **Factorización LU** (forma de Doolittle).
- **Factorización de Cholesky** (LLᵀ) para matrices simétricas definidas positivas. Aprovechando la simetría, solo se calcula la parte triangular inferior y en el remonte se accede a los elementos simétricos, sin construir Lᵀ.
- **Factorización LU para matrices tridiagonales.** La matriz se almacena únicamente en tres vectores (diagonales inferior, principal y superior) y en ningún momento se construye la matriz completa, lo que reduce el coste en memoria y en operaciones de O(n²) y O(n³) a O(n).

En todas las factorizaciones el resultado se almacena **sobre la propia matriz de entrada**, ya que la matriz factorizada tiene la misma estructura que la original.

**Métodos iterativos**, que reciben la aproximación inicial, el número máximo de iteraciones y la tolerancia en el error relativo, y devuelven también el número de iteraciones realizadas:
- **Gauss-Seidel** para la resolución de sistemas.
- **Potencia iterada** para el cálculo del autovalor de mayor módulo y su autovector asociado, normalizando en cada paso para evitar desbordamientos.

## Verificación

Cada ejecución mide el **tiempo de CPU** del proceso (más estable que el tiempo de reloj frente a interferencias de otros procesos), calcula el error relativo frente a la solución de NumPy y el residuo relativo ‖Ax − b‖ / ‖b‖, y guarda el vector solución en un fichero de texto con el índice de cada componente. En todos los métodos los errores obtenidos son del orden de 10⁻¹⁶, es decir, de la precisión de la máquina.

## Requisitos y dependencias

- **Python 3**
- Librerías nativas de Python utilizadas: `time`, `sys`
- **NumPy**

## Estructura del proyecto

- `main.py`: archivo principal de control y selección de apartados.
- `data.py`: definición de los datos de prueba.
- `factorizaciones.py`: implementación de las descomposiciones (LU, Cholesky y tridiagonal).
- `resolución_sistemas.py`: funciones de descenso, remonte y resolución global de cada tipo de sistema.
- `metodos_iterativos.py`: método de Gauss-Seidel.
- `calculo_maximo_autovalor.py`: método de la potencia iterada para el cálculo del máximo autovalor y su autovector asociado.
- `func_auxiliares.py`: comprobación de resultados y escritura de soluciones.
- `docs/enunciado.pdf`: enunciado de la práctica.

## Ejecución

Para ejecutar la práctica, lanza el script principal seleccionando un número entre 1 y 5:

- **1**: LU
- **2**: Cholesky
- **3**: tridiagonal
- **4**: Gauss-Seidel
- **5**: potencia iterada

Ejemplo de ejecución para el apartado de LU:

```bash
python3 main.py 1
```

### Apreciaciones

Los resultados se sobrescriben en el fichero `.txt` correspondiente. Si se quieren conservar los de ejecuciones anteriores, basta con cambiar el modo de apertura a *append* (sustituir la `w` por una `a` en `func_auxiliares.py`):

```python
with open(nombre_archivo, "w", encoding="utf-8") as f:
```

Las matrices de entrada se definen en `data.py` y deben estar siempre en formato `np.array`.
