from netmiko import ConnectHandler
import time
import subprocess


######################CONEXION NETMIKO###########################
def establecer_conexion_netmiko(device_info):
    try:
        connection = ConnectHandler(**device_info)
        return connection
    except Exception as e:
        print(f"Error conectando a {device_info['ip']}: {e}")
        return None
#################################################################

######################CONEXION PARAMIKO##########################
def send_command(channel, command, wait_time=2, max_buffer=65535):
    """
    Envía un comando a través del canal y devuelve la respuesta.
    """
    channel.send(command + "\n")
    time.sleep(wait_time)  # Espera para asegurar que el comando se haya completado
    # Verifica si el canal está listo para recibir datos
    while not channel.recv_ready(): 
        time.sleep(0.5)
    response = channel.recv(max_buffer).decode('utf-8')
    return response

def interactive_send_command(channel, command, confirmation_text, response, wait_time=2):
    """
    Maneja interacciones que requieren una respuesta interactiva, como confirmaciones.
    """
    # Envía el comando inicial
    channel.send(command + "\n")
    time.sleep(wait_time)
    # Lee la respuesta inicial
    intermediate_response = channel.recv(9999).decode('utf-8')
    #print(intermediate_response)   
    # Si se detecta la solicitud de confirmación, envía la respuesta especificada
    if confirmation_text in intermediate_response:
        channel.send(response + "\n")
        time.sleep(wait_time)

    return channel.recv(9999).decode('utf-8')
#################################################################

######################CONEXION EPMIKO ##########################
def epmiko(networking, password, host, comandos):
    # Crear la lista de argumentos para el comando
    args = ['./b_id.sh', networking, password, host] + comandos

    try:
        # Ejecutar el comando y dejar que la salida se muestre directamente en la consola
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")