import subprocess

def epmiko(networking, password, host, comandos):
    """
    Funcion para realizar consulta de sh spaninng tree en switches TpLink
    Mediante Conexión STP, ejecuta un script en bash

    Paramters:
    networking(str):    Nombre de Usuario para conexion SSH
    password(str):      Contraseña para conexión SSH
    host(str):          Dirección IP del dispositivo
    comandos(str):      Comandos que permitiran consultar la información de STP

    Return:
    Crea un archivo de texto plano con la información de STP
    """
    # Asegúrate de que toda la indentación en esta función utiliza 4 espacios por nivel de indentación
    args = ['./tplink_auto.sh', networking, password, host, comandos] 
    try:
        # Ejecutar el comando y redirigir la salida al archivo
        with open('tplink_auto.txt', 'w') as output_file:
            subprocess.run(args, stdout=output_file, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al Consultar Datos de Switches TpLink: {e}")