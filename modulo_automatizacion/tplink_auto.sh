#!/usr/bin/expect -f
# Obtener el nombre de usuario, la contraseña, el host y el tipo de comando
set username [lindex $argv 0]
set password [lindex $argv 1]
set host [lindex $argv 2]
set commandsFile [lindex $argv 3]
# Leer comandos del archivo
set fileId [open $commandsFile r]
set commands [split [read $fileId] "\n"]
close $fileId

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
        # Iterar sobre la lista de comandos y ejecutarlos uno por uno
        foreach command $commands {
            send "$command\r"
            expect "#"
        }
    }
}
expect eof
