import psutil
import time
from datetime import datetime

# Función para ejecutar tu script (reemplaza esta función con el código de tu script)
def my_script():
    # Ejemplo de un script que consume CPU
    for _ in range(10**7):
        pass

# Monitorear el uso del CPU antes de ejecutar el script
cpu_percent_before = psutil.cpu_percent(interval=1)
print(f'Uso del CPU antes de ejecutar el script: {cpu_percent_before}%')

# Registrar el tiempo de inicio
start_time = datetime.now()

# Ejecutar el script y medir el uso del CPU durante su ejecución
print('Ejecutando el script...')
cpu_percent_during = []
for i in range(10):
    time.sleep(1)
    cpu_percent_during.append(psutil.cpu_percent(interval=1))
    print(f'Segundo {i+1}: Uso del CPU: {cpu_percent_during[-1]}%')

# Registrar el tiempo de finalización
end_time = datetime.now()

# Monitorear el uso del CPU después de ejecutar el script
cpu_percent_after = psutil.cpu_percent(interval=1)
print(f'Uso del CPU después de ejecutar el script: {cpu_percent_after}%')

# Calcular la duración del script
duration = end_time - start_time

# Imprimir resultados
print(f'Duración de la ejecución del script: {duration}')
print(f'Promedio del uso del CPU durante la ejecución del script: {sum(cpu_percent_during) / len(cpu_percent_during)}%')
