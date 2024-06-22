import subprocess

with open('pid.txt', 'r') as archivo:
    pids = eval(archivo.readline().strip())


def matar_proceso(pid):
    try:
        # Ejecuta el comando kill -9 PID para matar el proceso
        subprocess.run(['kill', '-9', str(pid)], check=True)
        print(f"Proceso con PID {pid} ha sido terminado.")
    except subprocess.CalledProcessError as e:
        print(f"No se pudo terminar el proceso con PID {pid}. Error:", e)

for i in pids:
    matar_proceso(i)