import zipfile
import shutil
import random
from django.conf import settings
import os
import mysql.connector

class Zip:
    #Función para descomprimir el dataset del archivo zip
    def descomprimirConstruido(rutaDataset, rutaOrigen, rutaDestino, formatoImg, nombreDataset, estructuraDataset):
        # Abrir archivo .zip en modo lectura
        zip = zipfile.ZipFile(rutaOrigen, 'r')

        # Descomprimir el archivo .zip en la ruta destino
        zip.extractall(rutaDestino)
        zip.close()

        # Eliminar archivo .zip de donde se extrajeron las imagenes
        os.remove(rutaOrigen)

        # Validar si las enfermedades estan dentro de otra carpeta
        if(estructuraDataset == 'Construido_Si_Carpeta'):
            nombre_otra_carpeta = os.listdir(rutaDestino)
            nueva_rutaDestino = os.path.join(rutaDestino, nombre_otra_carpeta[0])
            for enfermedad in os.listdir(nueva_rutaDestino):
                if os.path.isdir(os.path.join(nueva_rutaDestino, enfermedad)):
                    shutil.move(os.path.join(nueva_rutaDestino, enfermedad), rutaDestino)
            shutil.rmtree(nueva_rutaDestino)

        # Obtener la lista de enfermedades
        carpetas_enfermedades = [nombre for nombre in os.listdir(rutaDestino + "/train/") if os.path.isdir(os.path.join(rutaDestino, 'train', nombre))]
        
        total_img_dataset = []
        train_img_dataset = []
        validate_img_dataset = []
        test_img_dataset = [0]

        for division_carpetas in os.listdir(rutaDestino):

            for enfermedad in os.listdir(os.path.join(rutaDestino, division_carpetas)):
                
                # for i, archivo in enumerate(os.listdir(os.path.join(rutaDestino, division_carpetas, enfermedad))):
                if(division_carpetas == 'train'):
                    train_size = len(os.listdir(os.path.join(rutaDestino, division_carpetas, enfermedad)))
                    train_img_dataset.append(train_size)
                if(division_carpetas == 'validation'):
                    validate_size = len(os.listdir(os.path.join(rutaDestino, division_carpetas, enfermedad)))
                    validate_img_dataset.append(validate_size)
                if(division_carpetas == 'test'):
                    test_size = len(os.listdir(os.path.join(rutaDestino, division_carpetas, enfermedad)))
                    test_img_dataset.append(test_size)
                    
                    # # Renombrar archivos
                    # ruta_archivo = os.path.join(rutaDestino, division_carpetas, enfermedad, archivo)
                    # ruta_archivo_nuevo = os.path.join(rutaDestino, division_carpetas, enfermedad, enfermedad + str(i) + '.' + formatoImg)
                    # os.rename(ruta_archivo, ruta_archivo_nuevo)

                total_img_dataset.append(len(os.listdir(os.path.join(rutaDestino, division_carpetas, enfermedad))))

        # Actualizar los datos en la tabla datasets
        conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
        myquery=conection.cursor()
        myquery.execute("""UPDATE appsafecrops_dataset set ruta = %s, numImgTotal = %s, numImgEntrenamiento = %s, numImgValidacion = %s, numImgPrueba = %s, numClases = %s WHERE nombreDataset = %s""", ("datasets/"+nombreDataset, sum(total_img_dataset), sum(train_img_dataset), sum(validate_img_dataset), sum(test_img_dataset), len(carpetas_enfermedades), nombreDataset)) #se actualiza la ruta del dataset
        conection.commit() #se confirma la actualización
        myquery.close() #se cierra el cursor


    def descomprimirConstruir(rutaDataset, rutaOrigen, rutaDestino, formatoImg, nombreDataset, estructuraDataset):
        # Abrir archivo .zip en modo lectura
        zip = zipfile.ZipFile(rutaOrigen, 'r')

        # Descomprimir el archivo .zip en la ruta destino
        zip.extractall(rutaDestino)
        zip.close()

        # Validar si las enfermedades estan dentro de otra carpeta
        if(estructuraDataset == 'Construir_Si_Carpeta'):
            nombre_otra_carpeta = os.listdir(rutaDestino)
            nueva_rutaDestino = os.path.join(rutaDestino, nombre_otra_carpeta[0])
            for enfermedad in os.listdir(nueva_rutaDestino):
                if os.path.isdir(os.path.join(nueva_rutaDestino, enfermedad)):
                    shutil.move(os.path.join(nueva_rutaDestino, enfermedad), rutaDestino)
            shutil.rmtree(nueva_rutaDestino)

        # Obtener la lista de enfermedades
        carpetas_enfermedades = [nombre for nombre in os.listdir(rutaDestino) if os.path.isdir(os.path.join(rutaDestino, nombre))]
        
        total_img_dataset = []
        train_img_dataset = []
        validate_img_dataset = []
        test_img_dataset = []

        for carpeta_enfermedad in carpetas_enfermedades:
            #Obtener la lista de archivos en la carpeta de enfermedad
            archivos_enfermedad = os.listdir(os.path.join(rutaDestino, carpeta_enfermedad))

            # Revolver los archivos aleatoriamente para evitar sesgos en el modelo de aprendizaje
            random.shuffle(archivos_enfermedad)

            # Calcualr la cantidad de archivos para entrenamiento y validación
            total_archivos = len(archivos_enfermedad)
            train_size = int(total_archivos * 0.8)
            validate_size = int(total_archivos * 0.1)
            test_size = total_archivos - train_size - validate_size

            # Crear los directorios de entrenamiento y validación
            train_dir = os.path.join(rutaDestino, 'train', carpeta_enfermedad)
            validate_dir = os.path.join(rutaDestino, 'validation', carpeta_enfermedad)
            test_dir = os.path.join(rutaDestino, 'test', carpeta_enfermedad)

            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(validate_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            # Mover archivos a los directorios en entrenamiento y validación
            for i, archivo in enumerate(archivos_enfermedad):
                origen = os.path.join(rutaDestino, carpeta_enfermedad, archivo)
                if i < train_size:
                    destino = os.path.join(train_dir, carpeta_enfermedad + str(i) + '.' + formatoImg)
                elif i > train_size + validate_size:
                    destino = os.path.join(validate_dir, carpeta_enfermedad + str(i) + '.' + formatoImg)
                else:
                    destino = os.path.join(test_dir, carpeta_enfermedad + str(i) + '.' + formatoImg)
                shutil.copy(origen, destino)
                os.remove(origen)

            carpeta_enfermedad_origen = rutaDestino + "/" + carpeta_enfermedad
            shutil.rmtree(carpeta_enfermedad_origen)

            total_img_dataset.append(total_archivos)
            train_img_dataset.append(train_size)
            validate_img_dataset.append(validate_size)
            test_img_dataset.append(test_size)

        

        # Eliminar archivo .zip de donde se extrajeron las imagenes
        os.remove(rutaOrigen)

        # Actualizar los datos en la tabla datasets
        conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
        myquery=conection.cursor()
        myquery.execute("""UPDATE appsafecrops_dataset set ruta = %s, numImgTotal = %s, numImgEntrenamiento = %s, numImgValidacion = %s, numImgPrueba = %s, numClases = %s WHERE nombreDataset = %s""", ("datasets/"+nombreDataset, sum(total_img_dataset), sum(train_img_dataset), sum(validate_img_dataset), sum(test_img_dataset), len(carpetas_enfermedades), nombreDataset)) #se actualiza la ruta del dataset
        conection.commit() #se confirma la actualización
        myquery.close() #se cierra el cursor
        
        
        
