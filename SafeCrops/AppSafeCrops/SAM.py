# https://github.com/alexFocus92/youtube_projects/blob/main/how_to_segment_anything_with_sam.ipynb

import os
import sys
import pip
import subprocess
import wget
import torch
import cv2
import supervision as sv
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor


HOME = os.getcwd() # Directorio principal
print("Directorio principal: ", HOME)

path_weight = HOME+"/weights" # Directorio para guardar los pesos del modelo SAM
path_data = HOME+"/data" # Directorio para guardar las imágenes de prueba para segmentar

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_TYPE = "vit_h"

print("Device: ", DEVICE)

# Función para instalar paquetes necesarios
def install():
    try:
        subprocess.call([sys.executable, "-m", ".\DJSafeCrops\Scripts"+"/activate"]) #Activar entorno virtual
        subprocess.call([sys.executable, "-m", "pip", "install", "git+https://github.com/facebookresearch/segment-anything.git"]) #Instalar numpy con pip
        subprocess.call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"]) #Instalar numpy con pip
        subprocess.call([sys.executable, "-m", "pip", "install", "wget==3.2"])
        subprocess.call([sys.executable, "-m", "pip", "install", "torch==2.0.1"])
        subprocess.call([sys.executable, "-m", "pip", "install", "torchvision==0.15.2"])
        subprocess.call([sys.executable, "-m", "pip", "install", "opencv-python==4.7.0.72"])
        subprocess.call([sys.executable, "-m", "pip", "install", "matplotlib==3.7.2"])
        subprocess.call([sys.executable, "-m", "pip", "install", "supervision==0.14.0"])
    except:
        print("Error al instalar el paquete")

# Función para cambiar de directorio con try except
def cd(path):
    try:
        os.chdir(path)
        print("Directorio actual: ", os.getcwd())
    except:
        print("Error al cambiar de directorio ", path)


# Función para crear directorio de pesos
def create_weight_directory():
    if not os.path.exists(path_weight):
        try:
            os.mkdir(path_weight)
            print("El directorio weight ha sido creado correctamente")
        except:
            print("Error al crear el directorio de weights.!!!!")
    else:
        print("El directorio de weights ya existe")

# Función para descargar los pesos predeterminados de SAM
def download_sam_weights():
    if not os.path.exists("sam_vit_h_4b8939.pth"):
        wget.download('https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth')
    else:
        print("El archivo sam_vit_h_4b8939.pth ya se encuentra descargado")

# Función para seleccionar el archivo de checkpoints (pesos) a utilizar
def select_checkpoint():
    if os.path.exists("fine_tuned_sam.pth"): # Validar si existe el archivo de pesos propio para utilizarlo
        CHECKPOINT_PATH = os.path.join(HOME, "weights", "fine_tuned_sam.pth")
    else: # Si no, utlizar el de SAM por defecto
        CHECKPOINT_PATH = os.path.join(HOME, "weights", "sam_vit_h_4b8939.pth")

    print(CHECKPOINT_PATH, "; exist:", os.path.isfile(CHECKPOINT_PATH))
    
    return CHECKPOINT_PATH

# Función para crear directorio de datos
def create_data_directory():
    if not os.path.exists(path_data):
        try:
            os.mkdir(path_data)
            print("El directorio data ha sido creado correctamente")
        except:
            print("Error al crear el directorio de data.!!!")
    else:
        print("El directorio de data ya existe")

# Función para descargar los datos (imágenes para segmentar) de ejemplo
def download_example_data():
    try:
        if not os.path.exists("dog.jpeg"):
            wget.download('https://media.roboflow.com/notebooks/examples/dog.jpeg')
        else:
            print("El archivo ya se encuentra descargado")
        
        if not os.path.exists("dog-2.jpeg"):
            wget.download('https://media.roboflow.com/notebooks/examples/dog-2.jpeg')
        else:
            print("El archivo ya se encuentra descargado")

        if not os.path.exists("dog-3.jpeg"):
            wget.download('https://media.roboflow.com/notebooks/examples/dog-3.jpeg')
        else:
            print("El archivo ya se encuentra descargado")

        if not os.path.exists("dog-4.jpeg"):
            wget.download('https://media.roboflow.com/notebooks/examples/dog-4.jpeg')
        else:
            print("El archivo ya se encuentra descargado")
    except:
        print("Error al descargar los datos de ejemplo")

# Función para generar segmentación con cuadro delimitador
def generar_segmentacion_cuadro_delimitador():

    mask_predictor = SamPredictor(sam)

    plants_img = []

    dir = (HOME+"/data/campo/")
    imageContent = os.listdir(dir)
    for image in imageContent: # ciclo para imagenes
        if os.path.isfile(os.path.join(dir, image)):
            plants_img.append(image)
    print("Diccionario imagenes... ", plants_img)

    for nombre_planta in plants_img:
        
        IMAGE_NAME = nombre_planta
        IMAGE_PATH = os.path.join(dir, IMAGE_NAME)

        # Draw box
        def drawing_bbox(imagen):
            bbox = []
            imagen_copia = imagen.copy()

            def drawing_rectangle(event, x, y, flags, params):
                nonlocal bbox

                if event == cv2.EVENT_LBUTTONDOWN:
                    bbox = [(x, y)]
                
                elif event == cv2.EVENT_LBUTTONUP:
                    bbox.append((x, y))
                    cv2.rectangle(imagen_copia, bbox[0], bbox[1], (0, 255, 0), 2)
                    cv2.imshow('Imagen', imagen_copia)

            cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
            cv2.setMouseCallback('Imagen', drawing_rectangle)

            while True:
                cv2.imshow('Imagen', imagen_copia)
                key = cv2.waitKey(1) & 0xFF

                if key == ord('r'): # Reiniciar
                    imagen_copia = imagen.copy()
                    bbox = []

                if key == ord('q'): # Salir
                    break
                
                elif key == ord('c'): # Continuar
                    break

            cv2.destroyAllWindows()
            
            if len(bbox) == 2:
                return bbox[0], bbox[1]
            else:
                print("No se ha seleccionado ningún cuadro delimitador")
                return None

        imagen = cv2.imread(IMAGE_PATH)
        print("Mostrando imagen... ")
        coordenadas = drawing_bbox(imagen)

        print("Coordenadas del bbox obtenidas")

        box = np.array([
            coordenadas[0][0], # xmin
            coordenadas[0][1], # y min
            coordenadas[1][0], # x max
            coordenadas[1][1]  # y max
        ])

        image_bgr = cv2.imread(IMAGE_PATH)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        mask_predictor.set_image(image_rgb)

        masks, scores, logits = mask_predictor.predict(
            box=box,
            multimask_output=False #Estado inicial en True
        )

        # Visualizar los resultados con supervision
        box_annotator = sv.BoxAnnotator(color=sv.Color.red())
        mask_annotator = sv.MaskAnnotator(color=sv.Color.red())

        detections = sv.Detections(
            xyxy = sv.mask_to_xyxy(masks=masks),
            mask = masks,
        )
        detections = detections[detections.area == np.max(detections.area)]

        source_image = box_annotator.annotate(scene=image_bgr.copy(), detections=detections, skip_label=True)
        segmented_image = mask_annotator.annotate(scene=image_bgr.copy(), detections=detections)

        sv.plot_images_grid(
            images = [source_image, segmented_image],
            grid_size = (1, 2),
            titles = ["Original", "Segmentation"]
        )

        sv.plot_images_grid(
            images=masks,
            grid_size=(1, 4),
            size=(16, 4)
        )

        print("Todo correcto")
        path_save_model = HOME+"/weights"
        cd(path_save_model)
        print("Directorio actual:", os.getcwd())

        # Save the fine-tuned model
        torch.save(sam.state_dict(), 'fine_tuned_sam.pth')
    
        print("¡Segmentación con bbox exitosa!")
        
        

# Función para generar segmentación (máscaras) automáticamente
def generar_segmentacion_automatica():
    mask_generator = SamAutomaticMaskGenerator(sam)

    datasetName = "DataPrueba"
    dir = (HOME+"/SafeCrops/datasets/"+datasetName+"/train/")

    diseaseContent = os.listdir(dir)

    # Código para crear el diccionario que contiene las enfermedades del dataset
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

        # Nuevo directorio segmentado
        datasetNameSAM = datasetName+"_SAM"
        dirSAM = (HOME+"/SafeCrops/datasets/"+datasetNameSAM+"/train/"+diseaseName)

        if os.path.exists(dirSAM):
            cd(dirSAM)
        else:
            os.makedirs(dirSAM)
            cd(dirSAM)


        for image in diseases:
            #print(image)
            IMAGE_NAME = image
            IMAGE_PATH = os.path.join(dir,diseaseName,IMAGE_NAME)

            #Generar mascaras con el modelo SAM
            
            image_bgr = cv2.imread(IMAGE_PATH)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

            sam_result = mask_generator.generate(image_rgb)

            detections = sv.Detections.from_sam(sam_result = sam_result)
            detections = detections[detections.area == np.max(detections.area)]

            # Ordenar la lista de mayor area a menor area de las mascaras guardadas en sam_result
            sorted_sam_result = sorted(sam_result, key=lambda x: x['area'], reverse=True)

            # Declarar lista que guardara las mascaras (en este caso la de mayor tamaño solamente)
            masks = []

            # Recorrer ciclo for de las mascaras para obtener la segmentación de la máscara principal
            for mask in sorted_sam_result:
                masks.append(mask['segmentation'])
                break

            segmentation_mask = masks[0]
            binary_mask = np.where(segmentation_mask > 0.5, 1, 0)

            white_background = np.ones_like(image_rgb) * 255

            new_image = white_background * (1 - binary_mask[..., np.newaxis]) + image_rgb * binary_mask[..., np.newaxis]
            new_image = new_image.astype(np.uint8)
            plt.axis('off')

            plt.imsave(image,new_image)

            print("¡Segmentación automática exitosa! - " + diseaseName)


#  #  #  #  #  #  #  #  #  #  #
#   Llamada a las funciones   #
#  #  #  #  #  #  #  #  #  #  #

#install() #Instalar los paquetes necesarios para la segmentación con SAM
create_weight_directory() # Validar si existe el directorio para guardar los pesos
cd(path_weight) # Ingresar a la ruta de weights
download_sam_weights() # Validar si eya exiten los pesos predeterminados de SAM
checkpoint = select_checkpoint() # Seleccionar que archivo de checkpoints (pesos) se utilizará para segmentar
create_data_directory() # Validar si existe el directorio para guardar las imágenes de prueba 
cd(path_data) # Ingresar a la ruta de data
download_example_data() # Descargar las imagenes de prueba
cd(HOME+"/SafeCrops/imagenes")
# Cargar el modelo
sam = sam_model_registry[MODEL_TYPE](checkpoint=checkpoint).to(device=DEVICE).train()
generar_segmentacion_cuadro_delimitador() # Segmentar dibujando un cuadro delimitador de forma manual
generar_segmentacion_automatica() # Segmentar de forma automática tomando la figura con mayor area dentro de la imagen


