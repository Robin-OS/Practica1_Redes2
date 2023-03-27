# Programa cliente
import os
import socket
import pathlib
from pathlib import Path
import zipfile
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

Tk().withdraw()
HOST = 'localhost'  # IP servidor
PORT = 8001        # Puerto en el que el servidor está escuchando

# Crea dos socket de tipo cliente


# Conéctate al servidor

main_flag = True
while main_flag:
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((HOST, PORT))
    cliente_socket_2.connect((HOST, 8002))
    # Menu para elegir accion
    print("Menu: \n 1. Enviar archivo \n 2. Descargar archivo")
    print(" 3. Borrar archivo \n 4. Borrar carpeta ")
    print(" 5. Crear nueva carpeta \n 6. Crear nuevo archivo ")
    print(" 7. Renombrar archivo o carpeta\n 8. Envio de multiples archivos ")
    print(" 9. Salir y cerrar todo ")
    menu = input('')
    cliente_socket.send(menu.encode())

    # Para envio de archivos
    if menu == '1':
        # Ver los archivos en una carpeta
        ruta = input("Introduce la ruta de la carpeta: ")
        archivos = os.listdir(ruta)
        print("Archivos en la carpeta:")
        for i, archivo in enumerate(archivos):
            print(f"{i+1}. {archivo}")

        # Seleccionar archivo
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
        cliente_socket.close()

    # Descarga de archivos
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
            with open(FILENAME, 'wb') as f:  # Abrir en modo de escritura
                # Recibe los datos del archivo en pequeñas partes
                while True:
                    datos = cliente_socket.recv(1024)
                    if not datos:
                        break
                    f.write(datos)

            print('Archivo recibido exitosamente.')
            cliente_socket.close()
            cliente_socket_2.close()



    # Eliminar archivos
    elif menu == '3':

        # Ver los archivos en una carpeta
        ruta = input("Introduce la ruta de la carpeta: ")
        archivos = os.listdir(ruta)  # Enlista los archivos de dicha ruta
        print("Archivos en la carpeta:")
        for i, archivo in enumerate(archivos):
            print(f"{i+1}. {archivo}")

        # Seleccionar archivo
        seleccion = input("Selecciona un archivo por número: ")
        archivo_seleccionado = ruta / archivos[int(seleccion)-1]
        print(f"Has seleccionado el archivo {archivo_seleccionado}")

        # Envío del nombre del archivo al servidor
        cliente_socket.send(archivo_seleccionado.encode())
        seg = input("¿Estas seguro de querer borrar el archivo?[S/N]: ")
        cliente_socket.send(seg.encode())
        respuesta = cliente_socket.recv(1024).decode()
        # print(archivo_seleccionado.encode())
        cliente_socket.close()


    # Eliminar carpetas
    elif menu == '4':

        # Ver las subcarpetas en una carpeta
        ruta = pathlib.Path(input("Introduce la ruta de la carpeta: "))
        # noinspection PyTypeChecker
        archivos = [ruta / archivo for archivo in os.listdir(ruta) if (ruta / archivo).is_dir()]
        # Enlista las carpetas de dicha ruta

        print("\n Subcarpetas en la carpeta:")
        for i, archivo in enumerate(archivos):
            print(f"{i + 1}. {archivo}")
        # Seleccionar carpeta
        seleccion = input("Selecciona una carpeta por número: ")
        carpeta_seleccionada = ruta / archivos[int(seleccion) - 1]
        ruta_carpselect = str(carpeta_seleccionada).encode()
        print(f"Has seleccionado la carpeta {carpeta_seleccionada}")
        carpetas = [carpeta_seleccionada / archivo for archivo in os.listdir(carpeta_seleccionada)]

        if len(carpetas) == 0:
            flag = -1
            flagt = str(flag).encode()
            print("\n Carpeta vacia")
        else:
            flag = 1
            flagt = str(flag).encode()
            print("\n Carpeta con elementos")
        # Envío de ruta de carpeta
        cliente_socket.send(ruta_carpselect)
        # Envío de la flag
        cliente_socket.send(flagt)
        # Recibe confirmación de borrado
        answ = cliente_socket.recv(1024).decode()
        print(answ)
        cliente_socket.close()


    # Crear carpetas
    elif menu == '5':
        direccion_act = Path(os.getcwd())
        direct_actual = input("¿Desea crear la carpeta en el directorio actual? [S/N]: ")
        if direct_actual == 'S' or direct_actual == 's':
            nombre_carpeta = input("Ingrese el nombre que tendra la carpeta: ")
            ruta_f = str(direccion_act / nombre_carpeta).encode()
        elif direct_actual == 'N' or direct_actual == 'n':
            ruta = Path(input("Ingrese la nueva ruta: "))
            nombre_carpeta = input("Ingrese el nombre que tendra la carpeta: ")
            ruta_f = str(ruta / nombre_carpeta).encode()
        else:
            print("Opcion invalida")
            ruta_f = None
        cliente_socket.send(ruta_f)
        answ = cliente_socket.recv(1024).decode()
        print(answ)
        cliente_socket.close()


    # Crear nuevo archivo
    elif menu == '6':
        direccion_act = Path(os.getcwd())
        direct_actual = input("¿Desea crear el archivo en el directorio actual? [S/N]: ")
        if direct_actual == 'S' or direct_actual == 's':
            nombre_archivo = input("Ingrese el nombre que tendra su archivo con la extension (.txt, .pdf, .docx...): ")
            ruta_f = str(direccion_act / nombre_archivo).encode()
        elif direct_actual == 'N' or direct_actual == 'n':
            ruta = Path(input("Ingrese la nueva ruta: "))
            nombre_archivo = input("Ingrese el nombre que tendra su archivo: ")
            ruta_f = str(ruta / nombre_archivo).encode()
        else:
            print("Opcion invalida")
            ruta_f = None
        cliente_socket.send(ruta_f)
        answ = cliente_socket.recv(1024).decode()
        print(answ)
        cliente_socket.close()


    # Renombrar archivo o carpeta
    elif menu == '7':
        direccion_act = Path(os.getcwd())
        direct_actual = input("¿Su archivo/carpeta se encuentra en el directorio actual? [S/N]: ")
        if direct_actual == 'S' or direct_actual == 's':
            nombre_archivo = input("Ingrese el nombre de su arch/car con extension (.txt, .pdf, .docx...): ")
            nuevo_nombre = input("Ingrese el nuevo nombre con extension si la hay: ")
            renombre = str(direccion_act / nuevo_nombre).encode()
            ruta_f = str(direccion_act / nombre_archivo).encode()
        elif direct_actual == 'N' or direct_actual == 'n':
            ruta = Path(input("Ingrese la ruta de su archivo a modificar: "))
            nombre_archivo = input("Ingrese el nombre su arch/car con extension: ")
            nuevo_nombre = input("Ingrese el nuevo nombre con extension si la hay: ")
            renombre = str(ruta / nuevo_nombre).encode()
            ruta_f = str(ruta / nombre_archivo).encode()
        else:
            print("Opcion invalida")
            ruta_f = None
            renombre = None
        cliente_socket.send(ruta_f)
        cliente_socket.send(renombre)
        answ = cliente_socket.recv(1024).decode()
        print(answ)
        cliente_socket.close()

    elif menu == '8':
        file_paths = askopenfilenames()
        carpeta = input("Ingrese el nombre para la carpeta: ") + ".zip"
        with zipfile.ZipFile(carpeta, 'w') as myzip:
            # Agrega cada archivo seleccionado al archivo .zip
            for path in file_paths:
                myzip.write(path, os.path.basename(path))
        print('Archivos comprimidos exitosamente.')
        cliente_socket.send(carpeta.encode())
        # Envio del archivo al servidor
        with open(carpeta, 'rb') as archivo:
            datos = archivo.read(1024)
            while datos:
                cliente_socket.send(datos)
                datos = archivo.read(1024)
        print('Archivo enviado exitosamente.')
        cliente_socket.close()

    elif menu == '9':
        main_flag = False
        cliente_socket.close()
