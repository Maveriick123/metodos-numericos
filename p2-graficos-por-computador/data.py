"""
* Datos del enunciado. Los puntos se definen como np.array de floats.
"""

import numpy as np

# -------------------------------------------------------------
# Ejercicio 1. Spline cúbico
# -------------------------------------------------------------
x_spline = np.array([-2.0, -1.5, 0.0, 1.0, 2.5, 4.0, 5.5, 7.0, 8.0, 10.0], dtype=float)
w_spline = np.array([ 0.0, -1.0, 1.0, -1.0, -2.0, 4.0, 3.0, 3.0, -2.0, 0.0], dtype=float)

# Condiciones adicionales: S''(x_0) = -2  y  S''(x_n) = 0
# Como S''(x_i) = c_i, estas condiciones fijan c_0 y c_n
c0_spline = -2.0
cn_spline = 0.0


# -------------------------------------------------------------
# Ejercicios 2 y 3. Puntos de control c_0, ..., c_16
# -------------------------------------------------------------
# Cada fila es un punto (x_k, y_k) -> matriz de 17 filas y 2 columnas
puntos_control = np.array([
    [-2.0, -2.0],   # c_0
    [-3.0, -2.0],   # c_1
    [-2.0,  0.0],   # c_2
    [-4.0,  1.0],   # c_3
    [-3.0,  4.0],   # c_4
    [-2.0,  4.0],   # c_5
    [-1.0,  3.0],   # c_6
    [ 1.0,  5.0],   # c_7
    [ 3.0,  3.0],   # c_8
    [ 2.0,  0.0],   # c_9
    [ 0.0,  0.0],   # c_10
    [-1.0,  2.0],   # c_11
    [ 1.0,  2.0],   # c_12
    [ 4.0,  1.0],   # c_13
    [ 3.0, -2.0],   # c_14
    [ 2.0, -3.0],   # c_15
    [-1.0, -2.0],   # c_16
], dtype=float)

# 2(b): grupos de puntos de control (índices inicial y final, ambos incluidos)
rangos_tramos = [(0, 5), (6, 12), (13, 16)]
nombres_tramos = ["I (c0-c5)", "II (c6-c12)", "III (c13-c16)"]

# 2(d): curva racional con los puntos c_2, ..., c_11
# El enunciado no fija los pesos, se da más peso (3) a las esquinas del polígono
# (c_3, c_7 y c_9) para que la curva se acerque a ellas // el resto vale 1.
# Cuanto más peso, más cerca de los puntos de control.
indices_racional = list(range(2, 12))
pesos_racional = np.array([1.0, 3.0, 1.0, 1.0, 1.0, 3.0, 1.0, 3.0, 1.0, 1.0], dtype=float)
#                          c2   c3   c4   c5   c6   c7   c8   c9   c10  c11

# 2(e): puntos a interpolar (x, y, z)
puntos_interpolar = np.array([
    [0.0,  1.0000,  0.0000],
    [0.0,  0.7071,  0.7071],
    [0.2,  0.0000,  1.0000],
    [0.4, -0.7071,  0.7071],
    [0.6, -1.0000,  0.0000],
    [0.8, -0.7071, -0.7071],
    [1.0, -0.0000, -1.0000],
    [1.2,  0.7071, -0.7071],
    [1.4,  1.0000, -0.0000],
    [1.6,  0.7071,  0.7071],
    [1.8,  0.0000,  1.0000],
    [2.0, -0.7071,  0.7071],
    [2.2, -1.0000,  0.0000],
    [2.4, -0.7071, -0.7071],
    [2.6, -0.0000, -1.0000],
    [2.8,  0.7071, -0.7071],
    [3.0,  1.0000, -0.0000],
], dtype=float)

# -------------------------------------------------------------
# Ejercicio 3. B-spline cúbico
# -------------------------------------------------------------
grado_bspline = 3
