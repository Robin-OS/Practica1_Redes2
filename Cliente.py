import socket
import os

HOST = 'localhost'  # IP servidor
PORT = 8001        # Puerto en el que el servidor está escuchando

# Crea dos socket de tipo cliente
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket_2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Conéctate al servidor
cliente_socket.connect((HOST, PORT))
cliente_socket_2.connect((HOST,8002))

#Menu para elegir accion
while True:
    menu = input("Menu: \n 1. Enviar archivo \n 2. Descargar archivo \n")
    cliente_socket.send(menu.encode())

    #Para envio de archivos
    if menu == '1':
        # Ver los archivos en una carpeta
        ruta = input("Introduce la ruta de la carpeta: ")
        archivos = os.listdir(ruta)
        print("Archivos en la carpeta:")
        for i, archivo in enumerate(archivos):
            print(f"{i+1}. {archivo}")

        #seleccionar archivo
        seleccion = input("Selecciona un archivo por número: ")
        archivo_seleccionado = archivos[int(seleccion)-1]
        print(f"Has seleccionado el archivo {archivo_seleccionado}")

        # Envío del nombre del archivo al servidor
        cliente_socket.send(archivo_seleccionado.encode())

        # Envio del archivo al servidor
        with open(archivo_seleccionado, 'rb') as archivo:
            datos = archivo.read(1024)
            while datos:
                cliente_socket.send(datos)
                datos = archivo.read(1024)

        print('Archivo enviado exitosamente.')

    #Descarga de archivos
    elif menu == '2':

        mensajes = cliente_socket_2.recv(1024).decode()
        print(mensajes)
        mensajes = cliente_socket_2.recv(1024).decode()
        print(mensajes)
        # enviar el nombre del archivo a descargar
        FILENAME = input("Escriba el nombre del archivo a descargar: ")
        cliente_socket.sendall(FILENAME.encode())

        # recibir la respuesta del servidor
        respuesta = cliente_socket.recv(1024).decode()
        print(respuesta)
        if respuesta == "archivo no encontrado":
            print("El archivo solicitado no se encontró en el servidor")
        else:
            with open(FILENAME, 'wb') as f: #Abrir en modo de escritura
                # Recibe los datos del archivo en pequeñas partes
                while True:
                    datos = cliente_socket.recv(1024)
                    if not datos:
                        break
                    f.write(datos)

            print('Archivo recibido exitosamente.')


# Cierra la conexión y el socket del cliente
cliente_socket.close()