import matplotlib.pyplot as plt

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
tiempo_configuracion = [
    37.44,
    33.1522,
    38.3089,
    31.85,
    31.38,
    31.088,
    10.2811
]

# Colores en tonos de gris oscuros
colores = ['#333333', '#4d4d4d', '#666666', '#808080', '#999999', '#b3b3b3', '#cccccc']

# Crear gráfico
plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(servicios)), tiempo_configuracion, color=colores)
plt.xlabel('Servicio')
plt.ylabel('Tiempo de Configuración [segundos]')
plt.title('Servicio vs Tiempo de Configuración')

# Personalizar nombres del eje x
plt.xticks(range(len(servicios)), servicios, rotation=45, ha='right')

# Eliminar cuadrícula
plt.grid(False)

# Mostrar valores en las barras
for bar, valor in zip(bars, tiempo_configuracion):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{valor:.2f}', ha='center', va='bottom')

# Mostrar gráfico
plt.tight_layout()
plt.show()
