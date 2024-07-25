import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Datos proporcionados
datos_2_cpu= [19.7, 10.3, 14.7, 9.3, 10, 7.7, 6.3, 11, 12.3, 10.3, 10.7, 11, 9.7, 10.3, 9.7, 10.3, 10.6, 10, 11.3, 12.6, 12, 9.7, 10.3, 9.7, 9.3]
datos_3_cpu = [27.7, 18, 19, 18, 15.7, 15, 13, 9, 13.3, 13, 16.3, 17.3, 16.3, 17, 16, 21, 14, 11, 14.7, 13.7, 14.7, 15, 15.7, 16, 15.6]
datos_4_cpu = [26.7, 20.7, 17.7, 21, 28.6, 19.6, 18.7, 24.6, 21, 12.3, 20, 23.3, 26.3, 16.3, 25.3, 21, 11.3, 18.9, 25.3, 21.3, 12, 18.3, 21.3, 25, 12]
datos_5_cpu = [31.7, 23.3, 26.3, 25.3, 20, 26.7, 17.3, 33, 21.3, 22.6, 26.6, 17.3, 27.2, 17.3, 22, 25.9, 18, 25.9, 23.7, 21.3, 25.7, 20.9, 25.7, 16.3, 20]
datos_6_cpu = [28.2, 32, 25.3, 23.6, 17.7, 30.3, 26, 20.6, 22.3, 28, 22, 23.9, 28, 22.7, 20.7, 25.9, 32, 25.7, 22.3, 22.7, 27, 22.3, 20, 28.3, 25]
# Calcular estadísticas
medias_cpu = [np.mean(datos) for datos in [datos_2_cpu, datos_3_cpu, datos_4_cpu, datos_5_cpu, datos_6_cpu]]
std_devs_cpu = [np.std(datos) for datos in [datos_2_cpu, datos_3_cpu, datos_4_cpu, datos_5_cpu, datos_6_cpu]]
cis_cpu = [1.96 * std / np.sqrt(len(datos_2_cpu)) for std in std_devs_cpu]

# Crear gráfica
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Dibujar línea con intervalos de confianza
x = [2, 3, 4, 5, 6]
plt.plot(x, medias_cpu, marker='o', color='navy', label='Media')
plt.fill_between(x, np.array(medias_cpu) - np.array(cis_cpu), np.array(medias_cpu) + np.array(cis_cpu), color='brown', alpha=0.2, label='Intervalo de confianza (95%)')

# Personalizar etiquetas y título
plt.xlabel('Número de dispositivos', fontsize=14)
plt.ylabel('Tiempo (segundos)', fontsize=14)
plt.title('Tiempo medio por número de dispositivos con intervalos de confianza', fontsize=16)
plt.xticks(ticks=x, labels=[str(i) for i in x], fontsize=12)
plt.yticks(fontsize=12)

# Añadir leyenda
plt.legend(fontsize=12)

# Mostrar gráfica
plt.tight_layout()
plt.show()
