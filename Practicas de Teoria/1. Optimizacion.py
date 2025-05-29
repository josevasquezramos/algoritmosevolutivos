from scipy.optimize import linprog

# Coeficientes de la función objetivo (negativos porque linprog minimiza)
# Queremos maximizar 50x + 80y, equivalente a minimizar -50x - 80y
c = [-50, -80]

# Matriz de coeficientes para las desigualdades (Ax <= b)
# Restricciones:
# 2x + 3y <= 120
# -x <= -10  (que es x >= 10)
# -y <= -5   (que es y >= 5)
A = [
    [2, 3],
    [-1, 0],
    [0, -1]
]

b = [120, -10, -5]

# No hay restricciones explícitas de no-negatividad adicionales, pero linprog las asume por defecto
# Dado que x,y >= 0, y ya tenemos x >= 10, y >= 5 por las restricciones, está cubierto

# Ejecutar el solver
resultado = linprog(c, A_ub=A, b_ub=b, method='highs')

if resultado.success:
    x_opt, y_opt = resultado.x
    ganancia_max = -resultado.fun  # Recordar que minimizamos el negativo de la función objetivo
    print(f"Producción óptima:")
    print(f"Artesanía A (x) = {x_opt:.2f} unidades")
    print(f"Artesanía B (y) = {y_opt:.2f} unidades")
    print(f"Ganancia máxima = S/ {ganancia_max:.2f}")
else:
    print("No se encontró solución óptima")
