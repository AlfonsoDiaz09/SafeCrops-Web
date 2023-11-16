import os
import mysql.connector

HOME = os.getcwd() # Directorio principal

# Función para cambiar de directorio con try except
def cd(path):
    try:
        os.chdir(path)
        print("Directorio actual: ", os.getcwd())
    except:
        print("Error al cambiar de directorio ", path)

def query_ruta_dataset(nombreDataset2):
    # Consultar ruta de dataset
    conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
    query = conection.cursor()

    query.execute("""SELECT ruta, numClases FROM appsafecrops_dataset WHERE nombreDataset = %s""", (nombreDataset2,)) #se obtiene la ruta del dataset
    result = query.fetchone()
    
    ruta = result[0]
    num = result[1]
   
    ruta = os.path.join(HOME, ruta)
    
    clases = []
    for nomClase in os.listdir(os.path.join(ruta,"train")):
        if os.path.isdir(os.path.join(ruta,"train",nomClase)):
            clases.append(nomClase)
    return ruta, num, clases
