import matplotlib.pyplot as plt
import numpy as np

# Datos
servicios = [
    'Lista de Acceso',
    'Comunidad SNMP',
    'Activar modo STP',
    'Prioridad Puente',
    'Costo de Ruta',
    'VLANs',
    'Logs'
]
tiempo_configuracion_automatica = [
    37.44,
    33.1522,
    38.3089,
    31.85,
    31.38,
    31.088,
    10.2811
]
tiempo_configuracion_manual = [
    240,
    180,
    480,
    300,
    240,
    180,
    300
]

# Colores
colores_automatico = '#6baed6'  # Azul claro
colores_manual = '#fdae6b'  # Naranja claro

# Crear gráfico
fig, ax = plt.subplots(figsize=(12, 6))

# Crear posiciones para las barras
x = np.arange(len(servicios))
width = 0.35

bars_auto = ax.bar(x - width/2, tiempo_configuracion_automatica, width, label='Automatización', color=colores_automatico)
bars_manual = ax.bar(x + width/2, tiempo_configuracion_manual, width, label='Manual', color=colores_manual)

# Etiquetas y título
ax.set_xlabel('Servicio', fontsize=14)
ax.set_ylabel('Tiempo de Configuración [segundos]', fontsize=14)
ax.set_title('Comparación de Tiempos de Configuración: Automatización vs Manual', fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(servicios, rotation=0, ha='center', fontsize=12)
ax.legend(fontsize=12)

# Mostrar valores en las barras
for bar_auto, bar_manual, valor_auto, valor_manual in zip(bars_auto, bars_manual, tiempo_configuracion_automatica, tiempo_configuracion_manual):
    ax.text(bar_auto.get_x() + bar_auto.get_width() / 2, bar_auto.get_height() + 0.5, f'{valor_auto:.2f}', ha='center', va='bottom', fontsize=10, color='black')
    ax.text(bar_manual.get_x() + bar_manual.get_width() / 2, bar_manual.get_height() + 0.5, f'{valor_manual:.2f}', ha='center', va='bottom', fontsize=10, color='black')

# Eliminar cuadrícula
ax.grid(False)

# Ajustar diseño para evitar recortes de etiquetas
plt.tight_layout()

# Mostrar gráfico
plt.show()
