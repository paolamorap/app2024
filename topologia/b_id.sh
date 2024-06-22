#!/usr/bin/expect -f

# Obtener el nombre de usuario y la contraseña
set username [lindex $argv 0]
set password [lindex $argv 1]

# Obtener la lista de hosts
set hosts [lrange $argv 2 end]

# Iterar sobre cada host en la lista
foreach host $hosts {
        # Imprimir el host actual
    puts "Conectando al host: $host"
    # Comando plink para conectar mediante SSH al host actual
    spawn plink -ssh -l $username -pw $password $host

    # Esperar a que aparezca la pregunta sobre continuar con la conexión
    expect {
        "Continue with connection? (y/n)" {
            send "y\r"
            exp_continue
        }
        "Further authentication required" {
            send "\r"
            exp_continue
        }
        "Access granted. Press Return to begin session." {
            send "\r"
            exp_continue
        }
        ">" {
            send "enable\r"
            exp_continue
        }
        "#" {
            send "sh spanning-tree active\r"
            # No hay necesidad de continuar, terminamos aquí
                 # Esperar cualquier texto después del prompt #
            expect -re ".+"
            # Mandar un enter
            send "\r"
	    expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"

            expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"

            expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"
            expect -re ".+"
            # Mandar un enter
            send "\r"

        }
    }
    close
}