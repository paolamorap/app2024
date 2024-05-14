from netmiko import ConnectHandler
import time
import subprocess
#********************************************************************************************
#------------------------------------- CONEXIONES SSH ---------------------------------------
#********************************************************************************************

#--------------------------------------------------------------------------------------------
#************************************ CONEXION NETMIKO **************************************
#--------------------------------------------------------------------------------------------
def establecer_conexion_netmiko(device_info):
    """
    Establece una conexión SSH con un dispositivo de red utilizando la biblioteca Netmiko.

    Esta función intenta realizar una conexión SSH a un dispositivo de red especificado en el 
    diccionario 'device_info'. Utiliza la biblioteca Netmiko, que soporta una variedad de 
    dispositivos de diferentes fabricantes.

    Parámetros:
        device_info (dict): Diccionario con la información necesaria para establecer la conexión:
            - device_type (str): Tipo de dispositivo según lo reconoce Netmiko (ej. 'cisco_ios', 'hp_comware').
            - host (str): Dirección IP del dispositivo.
            - username (str): Nombre de usuario para la autenticación SSH.
            - password (str): Contraseña para la autenticación SSH.
            - secret (str, opcional): Contraseña de modo privilegiado o enable password, si es necesario.

    Devuelve:
        Objeto ConnectHandler: Retorna un objeto de conexión si la conexión es exitosa, None en caso contrario.
    
    Excepciones:
        Imprime un mensaje de error si la conexión no se puede establecer y retorna None.
    """
    try:
        connection = ConnectHandler(**device_info)
        return connection
    except Exception as e:
        # Corrección: se debe asegurar que 'ip' existe en device_info para usarlo en el mensaje de error
        host = device_info.get('host', 'el dispositivo')
        print(f"Error conectando a {host}: {e}")
        return None


#--------------------------------------------------------------------------------------------
#*********************************** CONEXION PARAMIKO **************************************
#--------------------------------------------------------------------------------------------
def send_command(channel, command, wait_time=2, max_buffer=65535):
    """
    Envía un comando a través de un canal interactivo y espera por una respuesta.
    
    Esta función envía un comando al canal especificado, espera un período de tiempo para
    permitir que el comando se ejecute y luego recupera la respuesta hasta un límite máximo de bytes.
    
    Parámetros:
        channel: Objeto de canal interactivo a través del cual se envía el comando. 
        command (str): Comando en texto plano que se desea enviar al canal.
        wait_time (int, opcional): Tiempo en segundos que se espera después de enviar el comando antes de
                                   comenzar a recibir la respuesta. El valor predeterminado es 2 segundos.
        max_buffer (int, opcional): Máximo número de bytes que se leerán de la respuesta del canal.
                                    El valor predeterminado es 65535 bytes.
    Devuelve:
        str: La respuesta obtenida del canal después de ejecutar el comando.
    """
    channel.send(command + "\n")  # Envia el comando seguido de un salto de línea
    time.sleep(wait_time)  # Espera para permitir que el comando se procese en el canal

    # Espera hasta que el canal esté listo para recibir datos
    while not channel.recv_ready():
        time.sleep(0.5)

    # Recibe la respuesta del canal hasta el límite de max_buffer
    response = channel.recv(max_buffer).decode('utf-8')
    return response

def interactive_send_command(channel, command, confirmation_text, response, wait_time=2):
    """
    Envía un comando a través de un canal interactivo y maneja respuestas que requieren interacción,
    como las confirmaciones durante la ejecución del comando.

    Esta función es útil en situaciones donde el comando enviado requiere una interacción adicional,
    como confirmar una acción antes de proceder. La función espera una respuesta, verifica si se 
    necesita una confirmación adicional y, de ser así, envía una respuesta predeterminada.

    Parámetros:
        channel: Objeto de canal interactivo a través del cual se envía el comando y se reciben las respuestas.
        command (str): Comando en texto plano que se desea enviar.
        confirmation_text (str): Texto que se busca en la respuesta inicial para determinar si se requiere
                                 una acción de confirmación.
        response (str): Respuesta a enviar si se detecta el texto de confirmación.
        wait_time (int, opcional): Tiempo en segundos que se espera después de enviar el comando y la respuesta
                                   de confirmación, antes de proceder a la siguiente acción. Por defecto es 2 segundos.

    Devuelve:
        str: La respuesta final del canal después de manejar todas las interacciones necesarias.
    """
    channel.send(command + "\n")  # Envía el comando inicial seguido de un salto de línea
    time.sleep(wait_time)  # Espera para permitir que el comando se procese en el canal

    # Lee la respuesta inicial y decodifica a texto
    intermediate_response = channel.recv(9999).decode('utf-8')
    # Si se detecta el texto de confirmación en la respuesta, envía la respuesta especificada
    if confirmation_text in intermediate_response:
        channel.send(response + "\n")
        time.sleep(wait_time)  # Espera después de enviar la respuesta de confirmación

    # Recibe y devuelve la respuesta final del canal
    return channel.recv(9999).decode('utf-8')


#--------------------------------------------------------------------------------------------
#************************************ CONEXION EPMIKO ***************************************
#--------------------------------------------------------------------------------------------

def epmiko(user, password, host, comandos):
    """
    Ejecuta un script externo para interactuar con dispositivos TPLINK utilizando sus credenciales y comandos especificos 
    para la conexion SSH.

    Esta función verifica que ninguno de los parámetros sea None, prepara los argumentos necesarios, y ejecuta
    un script externo encargado de realizar operaciones en un dispositivo de red. La salida del script se redirige
    a un archivo para su revisión.

    Parámetros:
        user (str): Nombre de usuario para la autenticación en el dispositivo de red.
        password (str): Contraseña para la autenticación.
        host (str): Dirección IP o nombre de host del dispositivo.
        comandos (txt): Archivo txt con una secuencia de comandos a ejecutar en el dispositivo.

    Excepciones:
        ValueError: Se lanza si alguno de los parámetros es None.
        subprocess.CalledProcessError: Se lanza si el script externo falla (p.ej., termina con un código de error).
        Exception: Captura cualquier otra excepción que no sean las anteriores.

    """

    if None in [user, password, host, comandos]:
        raise ValueError(f"Uno de los argumentos de epmiko es None - usuario: {user}, contraseña: {password}, host: {host}, comandos: {comandos}")
    
    # Formar la lista de argumentos para el comando
    args = ['./tplink_auto.sh', user, password, host, comandos]

    # Intentar ejecutar el script externo y manejar excepciones
    try:
        # Abrir archivo de salida para redireccionar la salida del comando
        with open('tplink_auto.txt', 'w') as output_file:
            # Ejecutar el comando y capturar la salida
            subprocess.run(args, stdout=output_file, check=True)
    except subprocess.CalledProcessError as e:
        # Manejar el error si el proceso falla (p.ej., código de salida no es 0)
        print(f"Error al ejecutar el comando: {e}")
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(f"Ocurrió un error inesperado: {e}")

