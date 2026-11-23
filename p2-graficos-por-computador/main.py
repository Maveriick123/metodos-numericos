from spline import coeficientes_spline, comprobar_spline, representar_spline
from bezier import (curva_bezier, representar_bezier,
                    dividir_puntos, cerrar_curvas, representar_tramos,
                    curva_bezier_racional, representar_racional,
                    interpolar_bezier, representar_interpolacion)
from bspline import nodos_uniforme_abierto, curva_bspline, representar_bspline
import data
import sys

"""
Selección del apartado (argumento por línea de comandos):
1  --> Spline cúbico
2a --> Curva de Bézier (De Casteljau) con los 17 puntos de control
2b --> Tres curvas de Bézier (puntos 0-5, 6-12, 13-16)
2c --> Unión de las tres curvas en una curva cerrada
2d --> Curva de Bézier racional (puntos 2-11)
2e --> Curva de Bézier que interpola los puntos 3D
3  --> B-spline cúbico con nodos uniformes abiertos
"""

if len(sys.argv) > 1:
    SELECTION_FLAG = sys.argv[1]
else:
    SELECTION_FLAG = "1"


if SELECTION_FLAG == "1":
    c = coeficientes_spline(data.x_spline, data.w_spline, data.c0_spline, data.cn_spline)
    comprobar_spline(data.x_spline, data.w_spline, c)
    representar_spline(data.x_spline, data.w_spline, c)

elif SELECTION_FLAG == "2a":
    curva = curva_bezier(data.puntos_control)
    representar_bezier(data.puntos_control, curva, "Ejercicio 2(a): curva de Bézier (De Casteljau)")

elif SELECTION_FLAG == "2b":
    tramos = dividir_puntos(data.puntos_control, data.rangos_tramos)
    representar_tramos(tramos, data.nombres_tramos, "Ejercicio 2(b): tres curvas de Bézier")

elif SELECTION_FLAG == "2c":
    originales = dividir_puntos(data.puntos_control, data.rangos_tramos)
    tramos = cerrar_curvas(originales)
    representar_tramos(tramos, data.nombres_tramos, "Ejercicio 2(c): curva cerrada", originales)

elif SELECTION_FLAG == "2d":
    c = data.puntos_control[data.indices_racional]
    curva = curva_bezier_racional(c, data.pesos_racional)
    representar_racional(c, data.pesos_racional, curva, data.indices_racional,
                            "Ejercicio 2(d): curva de Bézier racional (puntos 2-11)")

elif SELECTION_FLAG == "2e":
    c = interpolar_bezier(data.puntos_interpolar)
    representar_interpolacion(data.puntos_interpolar, c, "Ejercicio 2(e): curva de Bézier interpolante")

elif SELECTION_FLAG == "3":
    n = data.puntos_control.shape[0] - 1
    u = nodos_uniforme_abierto(n, data.grado_bspline)
    curva = curva_bspline(data.puntos_control, u, data.grado_bspline)
    representar_bspline(data.puntos_control, u, data.grado_bspline, curva, "Ejercicio 3: B-spline cúbico")

else:
    print(f"Apartado '{SELECTION_FLAG}' no reconocido.")
