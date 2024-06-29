import matplotlib.pyplot as plt

# Tiempos de convergencia en segundos
tiempos = [27.24008916, 2.209538]
algoritmos = ['SSH', 'SNMP y STP']

# Colores tipo escala de grises
colores = [(0.6, 0.6, 0.6), (0.4, 0.4, 0.4)]

# Crear gráfico de barras
plt.figure(figsize=(8, 6))
bars = plt.bar(algoritmos, tiempos, color=colores)
plt.xlabel('Algoritmo')
plt.ylabel('Tiempo de Convergencia (segundos)')
#plt.title('Comparación de Tiempos de Convergencia')

# Mostrar valores en las barras
for bar, tiempo in zip(bars, tiempos):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(tiempo, 2), ha='center', va='bottom', fontsize=10)

# Eliminar cuadrícula interna
plt.grid(axis='y', which='both', color='gray', linestyle='-', linewidth=0.5)
plt.gca().yaxis.grid(False)

# Mostrar gráfico
plt.ylim(0, max(tiempos) * 1.1)  # Ajustar límites del eje y para mejor visualización
plt.tight_layout()
plt.show()
