import matplotlib.pyplot as plt

# Datos
algorithms = ['SSH', 'SNMP y STP']
times = [27.24, 2.21]

# Colores más vivos
colors = ['#6baed6', '#fdae6b']

# Crear la gráfica
fig, ax = plt.subplots()
bars = ax.bar(algorithms, times, color=colors)

# Añadir los valores encima de las barras
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom', fontsize=10)

# Añadir título y etiquetas
ax.set_title('Comparación de Tiempos de Convergencia', fontsize=13)
ax.set_xlabel('Algoritmo', fontsize=12)
ax.set_ylabel('Tiempo de Convergencia (segundos)', fontsize=12)

# Mostrar la gráfica
plt.show()
