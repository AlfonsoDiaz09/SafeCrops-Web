import os

HOME = os.getcwd() # Directorio principal

# Función para cambiar de directorio con try except
def cd(path):
    try:
        os.chdir(path)
        print("Directorio actual: ", os.getcwd())
    except:
        print("Error al cambiar de directorio ", path)