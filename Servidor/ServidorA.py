# Programa servidor
import socket
import os
import zipfile
from os import remove
from os import rmdir
from os import mkdir
from shutil import rmtree
from zipfile import ZipFile

FILEPATH = './Remota'
HOST = 'localhost'  # IP del servidor
PORT = 8001  # Puerto en el que escuchará el servidor

servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establecer un tiempo de espera infinito para recibir datos
servidor_socket.settimeout(None)
servidor_socket_2.settimeout(None)

# Vincula el socket al puerto y comienza a escuchar
servidor_socket.bind((HOST, PORT))
servidor_socket.listen()

servidor_socket_2.bind((HOST, 8002))
servidor_socket_2.listen()
print('Servidor en espera de conexiones...')

main_flag = True
while main_flag:


    # Acepta la conexión entrante
    cliente_socket, cliente_direccion = servidor_socket.accept()
    cliente_socket_2, cliente_direccion_2 = servidor_socket_2.accept()
    print('Conexión establecida desde', cliente_direccion)

    # Recibe la opcion del menu
    menu = cliente_socket.recv(1024).decode()

    # Para recibir archivo del cliente
    if menu == '1':
        # Recibe el nombre del archivo
        nombre_archivo = cliente_socket.recv(1024).decode()

        # Abre el archivo para escribir en el
        with open(nombre_archivo, 'wb') as archivo:
            while True:
                datos = cliente_socket.recv(1024)
                print("inifnio")
                if not datos:
                    print("ya me voy")
                    break
                archivo.write(datos)
        print('Archivo recibido exitosamente.')


    # Descarga de archivos para el cliente
    elif menu == '2':
        lista_archivos = []
        cliente_socket_2.sendall(b"ARCHIVOS REMOTOS: ")
        ruta = "./Remota"  # Envio de la lista de archivos en carpeta
        archivos = os.listdir(ruta)
        for i, archivo in enumerate(archivos):
            lista_archivos.append(f"{i + 1}.{archivo}")
        b = bytes(str(lista_archivos), 'utf-8')
        cliente_socket_2.sendall(b)

        # Recibe el nombre del archivo a descargar
        filename = cliente_socket.recv(1024).decode()
        filepath = os.path.join(FILEPATH, filename)

        # Si el archivo existe
        if os.path.exists(filepath):
            # envio
            with open(filepath, 'rb') as f:
                data = f.read(1024)
                while data:
                    cliente_socket.send(data)
                    data = f.read(1024)
            print(f"archivo {filename} enviado")

        # Si no existe
        else:
            print(f"No se encontro el archivo {filename}")
            cliente_socket.sendall(b"archivo no encontrado")
            cliente_socket.close()

    # Eliminar archivos
    elif menu == '3':
        # Recibe el nombre del archivo
        nombre_archivo = cliente_socket.recv(1024).decode()
        confirmacion = cliente_socket.recv(1024).decode()
        if confirmacion == 'S' or 's':
            remove(nombre_archivo)
            print("Se ha borrado el archivo ", nombre_archivo)
        else:
            cliente_socket.sendall(b"Archivo no borrado")

    # Eliminar carpetas
    elif menu == '4':
        # Recibe ruta de la carpeta
        nombre_carpeta = cliente_socket.recv(1024).decode()
        flagdeco = cliente_socket.recv(1024).decode()
        flag = int(flagdeco)
        if flag == -1:
            rmdir(nombre_carpeta)
            print("Se ha borrado la carpeta ", nombre_carpeta)
            cliente_socket.sendall(b"Se ha borrado la carpeta seleccionada")
        elif flag == 1:
            rmtree(nombre_carpeta)
            cliente_socket.sendall(b"Se ha borrado la carpeta seleccionada")

    # Crear carpetas
    elif menu == '5':
        direccion_Ncarpeta = cliente_socket.recv(1024).decode()
        print("Creando nueva carpeta...")
        mkdir(direccion_Ncarpeta)
        cliente_socket.sendall(b"Se ha creado la carpeta exitosamente")

    # Crear archivos
    elif menu == '6':
        # Se obtiene la ruta con el nombre del archivo
        direccion_Narchivo = cliente_socket.recv(1024).decode()
        print("Creando archivo...")
        # Sig linea crea archivo, tiene que abrirse en modo escritura
        with open(direccion_Narchivo, 'w') as file:
            print("Archivo creado")
        # With cierra automáticamente el archivo
        cliente_socket.sendall(b"Archivo creado exitosamente")

    # Renombrar archivo o carpeta
    elif menu == '7':
        # Se obtiene la ruta con el nombre del archivo
        dir_OldArchivo = cliente_socket.recv(1024).decode()
        dir_NewArchivo = cliente_socket.recv(1024).decode()
        print("Modificando archivo...")
        # Sig linea modifica archivo
        os.rename(dir_OldArchivo, dir_NewArchivo)
        cliente_socket.sendall(b"Archivo/Carpeta modificado exitosamente")

    elif menu == '8':
        nombre_archivo = cliente_socket.recv(1024).decode()

        # Abre el archivo para escribir en el
        with open(nombre_archivo, 'wb') as archivo:
            while True:
                datos = cliente_socket.recv(1024)
                if not datos:
                    break
                archivo.write(datos)
        print('Archivo recibido exitosamente.')
        carpeta = FILEPATH + "/" + nombre_archivo
        with ZipFile(file = nombre_archivo, mode="r", allowZip64=True) as file:
            archivo = file.open(name=file.namelist()[0],mode="r")
            #print(archivo.read())
            archivo.close()

            #print("descomprimiendo")
            file.extractall(path=carpeta)
            #print("Archivo descomprimido")

    elif menu == '9':
        ruta = FILEPATH
        lista_archivos = []
        for root, dirs, files in os.walk(ruta):
            for filename in files:
                lista_archivos.append(os.path.join(root, filename))
        b = bytes(str(lista_archivos), 'utf-8')
        #cliente_socket_2.sendall(b)
        longitud_lista = len(lista_archivos)
        longitud_lista = str(longitud_lista)
        longitud_l = bytes(longitud_lista.encode())
        cliente_socket_2.sendall(longitud_l)

        for i, f in enumerate(lista_archivos):
            # Obtener la carpeta actual
            current_folder = os.path.basename(os.path.dirname(f))
            # Tabular según la carpeta
            b = bytes(f"\t{current_folder}\t|\t{i + 1}\t|\t{os.path.basename(f)}\n", 'utf-8')
            cliente_socket_2.sendall(b)
        Archivos_comprimir = []
        while True:
            sel_archivos = cliente_socket_2.recv(1024).decode()
            if sel_archivos == 's':
                break
            try:
                indice = int(sel_archivos) - 1
                Archivos_comprimir.append(lista_archivos[indice])
                mensaje = bytes(f"El archivo {os.path.basename(lista_archivos[indice])} ha sido agregado a la lista de archivos a comprimir.",'utf-8')
                cliente_socket_2.sendall(mensaje)
            except:
                mensaje = bytes(f"Entrada no válida. Inténtalo de nuevo.", 'utf-8')
                cliente_socket_2.sendall(mensaje)

        # Comprimir los archivos seleccionados en un archivo zip

        zip_nombre= cliente_socket_2.recv(1024).decode()
        with zipfile.ZipFile(zip_nombre, 'w') as my_zip:
            for file_path in Archivos_comprimir:
                my_zip.write(file_path, os.path.basename(file_path))

        with open(zip_nombre, 'rb') as f:
            data = f.read(1024)
            while data:
                cliente_socket.send(data)
                data = f.read(1024)



    elif menu == 'E':
        main_flag = False
    # Cierra la conexión y el socket del servidor
    cliente_socket.close()

print("Fin del drive")
# servidor_socket.close()