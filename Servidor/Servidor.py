#Programa servidor
import socket
import os
FILEPATH = './Remota'
HOST = 'localhost'  # IP del servidor
PORT = 8001       # Puerto en el que escuchará el servidor

# Crea un socket de tipo servidor
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula el socket al puerto y comienza a escuchar
servidor_socket.bind((HOST, PORT))
servidor_socket.listen()

servidor_socket_2.bind((HOST, 8002))
servidor_socket_2.listen()
print('Servidor en espera de conexiones...')

# Acepta la conexión entrante
cliente_socket, cliente_direccion = servidor_socket.accept()
cliente_socket_2, cliente_direccion_2 = servidor_socket_2.accept()
print('Conexión establecida desde', cliente_direccion)

#Recibe la opcion del menu
menu = cliente_socket.recv(1024).decode()

#Para recibir archivo del cliente
if menu == '1':
    # Recibe el nombre del archivo
    nombre_archivo = cliente_socket.recv(1024).decode()

    # Abre el archivo para escribir en el
    with open(nombre_archivo, 'wb') as archivo:
        while True:
            datos = cliente_socket.recv(1024)
            if not datos:
                break
            archivo.write(datos)

    print('Archivo recibido exitosamente.')

#Descarga de archivos para el cliente
elif menu == '2':
    lista_archivos = []
    cliente_socket_2.sendall(b"ARCHIVOS REMOTOS: ")
    ruta = "./Remota"       #Envio de la lista de archivos en carpeta
    archivos = os.listdir(ruta)
    for i, archivo in enumerate(archivos):
        lista_archivos.append(f"{i + 1}.{archivo}")
    b = bytes(str(lista_archivos), 'utf-8')
    cliente_socket_2.sendall(b)

    #Recibe el nombre del archivo a descargar
    filename = cliente_socket.recv(1024).decode()
    filepath = os.path.join(FILEPATH,filename)

    #Si el archivo existe
    if os.path.exists(filepath):
        #envio
        with open(filepath, 'rb') as f:
            data = f.read(1024)
            while data:
                cliente_socket.send(data)
                data = f.read(1024)
        print(f"archivo {filename} enviado")

    #Si no existe
    else:
        print(f"No se encontro el archivo {filename}")
        cliente_socket.sendall(b"archivo no encontrado")



# Cierra la conexión y el socket del servidor
cliente_socket.close()
#servidor_socket.close()
