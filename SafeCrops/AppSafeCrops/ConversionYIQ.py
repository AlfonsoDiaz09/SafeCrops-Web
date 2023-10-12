# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:32:25 2023

@author: Deny
"""

import cv2
import numpy as np
import os
import torch

HOME = os.getcwd() # Directorio principal
print("Directorio principal: ", HOME)

path_weight = HOME+"/weights" # Directorio para guardar los pesos del modelo SAM
path_data = HOME+"/data" # Directorio para guardar las imágenes de prueba para segmentar

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_TYPE = "vit_h"

print("Device: ", DEVICE)

def cd(path):
    try:
        os.chdir(path)
        print("Directorio actual: ", os.getcwd())
    except:
        print("Error al cambiar de directorio")

def conversionYIQ(dir_diseases, referencia, conversion):
    imagen_ref = cv2.imread(dir_diseases+referencia) # Imagen de referencia
    imagen_conv = cv2.imread(dir_diseases+conversion) # Imagen a homogeneizar
    # Matriz de conversión YIQ
    matriz_yiq = np.array([[0.299, 0.587, 0.114],
                        [0.596, -0.274, -0.322],
                        [0.211, -0.523, 0.312]])
    print(imagen_ref)
    # Separar los canales BGR
    b, g, r = cv2.split(imagen_ref)
    b2, g2, r2 = cv2.split(imagen_conv)

    # Calcular los canales YIQ
    y = 0.299 * r + 0.587 * g + 0.114 * b
    i = 0.596 * r - 0.274 * g - 0.322 * b
    q = 0.211 * r - 0.523 * g + 0.312 * b
    y2 = 0.299 * r2 + 0.587 * g2 + 0.114 * b2
    i2= 0.596 * r2 - 0.274 * g2 - 0.322 * b2
    q2 = 0.211 * r2 - 0.523 * g2 + 0.312 * b2

    difMedY=np.mean(y)-np.mean(y2)
    difMedI=np.mean(i)-np.mean(i2)
    difMedQ=np.mean(q)-np.mean(q2)
    # Unir los canales YIQ en una imagen YIQ
    imagen_yiq_R = cv2.merge((y, i, q))

    y2=y2+difMedY
    i2=i2+difMedI
    q2=q2+difMedQ

    matriz_yiq_a_rgb = np.array([[1.0, 0.956, 0.621],
                                [1.0, -0.272, -0.647],
                                [1.0, -1.107, 1.705]])


    imagen_yiq_C = cv2.merge((y2, i2, q2))

    imagen_rgb = np.dot(imagen_yiq_C, matriz_yiq_a_rgb.T)
    imagen_rgb = np.clip(imagen_rgb, 0, 255).astype(np.uint8)
    imagen_bgr = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR)



    # Mostrar la imagen en el espacio de color YIQ
    #cv2.imshow('Imagen YIQ', imagen_bgr)

    # Esperar hasta que se presione una tecla y luego cerrar la ventana

    cv2.imwrite(conversion, imagen_bgr)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def colect_dataset():    
    datasetName = "DataPrueba"
    dir = (HOME+"/SafeCrops/datasets/"+datasetName+"/train/")

    diseaseContent = os.listdir(dir)

    diccionarioDataset = {}

    for disease in diseaseContent: # ciclo para enfermedades
        images = []
        dirImg = (dir+disease+"/")
        imageContent = os.listdir(dirImg)
        if os.path.isdir(os.path.join(dir, disease)):
            for image in imageContent: # ciclo para imagenes
                if os.path.isfile(os.path.join(dirImg, image)):
                    images.append(image)
            diccionarioDataset[disease] = images

    print(diccionarioDataset)

    for diseaseName in diccionarioDataset:

        diseases = diccionarioDataset[diseaseName]

        # Nuevo directorio YIQ
        datasetNameSAM = datasetName+"_YIQ2"
        dirSAM = (HOME+"/SafeCrops/datasets/"+datasetNameSAM+"/train/"+diseaseName)

        if os.path.exists(dirSAM):
            cd(dirSAM)
        else:
            os.makedirs(dirSAM)
            cd(dirSAM)


        for image in diseases:
            print(image)

            conversionYIQ(dir+diseaseName+"/", "leafRust32.jpg", image)


colect_dataset()