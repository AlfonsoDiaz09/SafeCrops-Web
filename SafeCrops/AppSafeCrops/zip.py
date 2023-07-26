import zipfile
import shutil
from django.conf import settings
import os
import mysql.connector

class Zip:
    #Función para descomprimir el dataset er archivo zip
    def descomprimir(rutaDataset,rutaName,tipo,numImgEntrenamiento,nombreDataset,imgTotal):
        rutaOrigen = settings.MEDIA_ROOT + 'datasets/' + rutaName
        rutaDestino = settings.MEDIA_ROOT + 'datasets/' + nombreDataset
        zip = zipfile.ZipFile(rutaOrigen, 'r')
        #Se crean las carpetas de entrenamiento y validacion
        zip.extractall(rutaDestino)
        listaImagenes = zip.namelist()
        os.mkdir(rutaDestino + '/entrenamiento')
        os.mkdir(rutaDestino + '/validacion')

        #Se mueven las imagenes a las carpetas de entrenamiento y validacion
        cont=0
        i=0
        for img in range(imgTotal):
            ruta_imagen = rutaDestino + '/' + listaImagenes[img]
            if cont < numImgEntrenamiento:
                shutil.copy(ruta_imagen, rutaDestino + '/entrenamiento/' + tipo + str(i) + '.jpg') #Se copia la imagen
                os.remove(ruta_imagen) #Se elimina la imagen
            else:
                shutil.copy(ruta_imagen, rutaDestino + '/validacion/' + tipo + str(i) + '.jpg')
                os.remove(ruta_imagen)
            cont = cont + 1
            i = i + 1
        zip.close()

        os.remove(rutaOrigen)

        conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
        last_id = conection.cursor() #se crea un cursor para obtener el id del ultimo dataset
        last_id.execute("""SELECT id_Dataset FROM appsafecrops_dataset ORDER BY id_Dataset DESC LIMIT 1""") #se obtiene el id del ultimo dataset
        id_dataset = last_id.fetchone()
        id_dataset = int(id_dataset[0])
        last_id.close() #se cierra el cursor

        myquery=conection.cursor() #se crea un cursor
        myquery.execute("""UPDATE appsafecrops_dataset set ruta = %s WHERE nombreDataset = %s""", ("datasets/"+nombreDataset, nombreDataset)) #se actualiza la ruta del dataset
        conection.commit() #se confirma la actualización
        myquery.close() #se cierra el cursor
        verificarCarpetaVacia = str(listaImagenes[0]).split('/')
        if len(verificarCarpetaVacia) >= 2:
            shutil.rmtree(rutaDestino + '/' + verificarCarpetaVacia[0]) #elimina una carpeta que no está vacia cuando el ZIP tenga una carpeta dentro
    
    
