# https://github.com/alexFocus92/youtube_projects/blob/main/how_to_segment_anything_with_sam.ipynb

import os
import sys
# # Variables globales
# print("Antes: ",os.getcwd())
# #sys.path.insert(1, '../')
# print("Despues: ",os.getcwd())
# #from GLOBAL_VARIABLES import HOME, cd
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

# Función para cambiar de directorio con try except
def cd(path):
    try:
        os.chdir(path)
        print("Directorio actual: ", os.getcwd())
    except:
        print("Error al cambiar de directorio ", path)

class SAM:
    def sam_automatico(nombreDataset):
        # Función para descargar los pesos predeterminados de SAM
        def download_sam_weights():
            if not os.path.exists("sam_vit_h_4b8939.pth"):
                wget.download('https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth')
            else:
                print("El archivo sam_vit_h_4b8939.pth ya se encuentra descargado")

        # Función para seleccionar el archivo de checkpoints (pesos) a utilizar
        def select_checkpoint():
            if os.path.exists("fine_tuned_sam.pth"): # Validar si existe el archivo de pesos propio para utilizarlo
                CHECKPOINT_PATH = os.path.join(HOME, 'AppSafeCrops', 'MODELO_SAM', "fine_tuned_sam.pth")
            else: # Si no, utlizar el de SAM por defecto
                CHECKPOINT_PATH = os.path.join(HOME, 'AppSafeCrops', 'MODELO_SAM', "sam_vit_h_4b8939.pth")

            print(CHECKPOINT_PATH, "; exist:", os.path.isfile(CHECKPOINT_PATH))
            
            return CHECKPOINT_PATH

        # Función para generar segmentación con cuadro delimitador
        #def generar_segmentacion_cuadro_delimitador():

            mask_predictor = SamPredictor(sam)

            plants_img = []

            datasetName = "DataPrueba"
            diseaseName = "Blueberry_Leaf Rust"

            dir = (HOME+"/SafeCrops/datasets/"+datasetName+"/train/"+diseaseName+"/")
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

                # sv.plot_images_grid(
                #     images = [source_image, segmented_image],
                #     grid_size = (1, 2),
                #     titles = ["Original", "Segmentation"]
                # )

                # sv.plot_images_grid(
                #     images=masks,
                #     grid_size=(1, 4),
                #     size=(16, 4)
                # )

                # Guardar imagen
                print("Comenzando proceso de guardado de imagen: "+nombre_planta)
                datasetNameSAM_bbox = datasetName+"_SAM_BBOX"
                dirSAM_bbox = (HOME+"/SafeCrops/datasets/"+datasetNameSAM_bbox+"/train/"+diseaseName+"/")

                if os.path.exists(dirSAM_bbox):
                    cd(dirSAM_bbox)
                else:
                    os.makedirs(dirSAM_bbox)
                    cd(dirSAM_bbox)


                segmentation_mask = masks
                binary_mask = np.where(segmentation_mask > 0.3, 1, 0)

                white_background = np.ones_like(image_rgb) * 255

                new_image = white_background * (1 - binary_mask[..., np.newaxis]) + image_rgb * binary_mask[..., np.newaxis]
                new_image = new_image.astype(np.uint8)
                plt.axis('off')
                plt.imshow(new_image)
                plt.imsave(nombre_planta,new_image)



                path_save_model = HOME+"/weights"
                cd(path_save_model)
                print("Directorio actual: ", os.getcwd())

                # Save the fine-tuned model
                torch.save(sam.state_dict(), 'fine_tuned_sam.pth')
            
                print("Pesos guardados fine_tuned_sam...")

                print("¡Segmentación con BBOX exitosa! - " + diseaseName)

        # Función para generar segmentación (máscaras) automáticamente
        def generar_segmentacion_automatica():
            mask_generator = SamAutomaticMaskGenerator(sam)

            datasetName = nombreDataset
            dir_dataset = os.path.join(HOME, 'datasets', datasetName)
            #dir = (HOME+"/SafeCrops/datasets/"+datasetName+"/train/")
            
            # Arreglo con extensiones de imagenes válidas
            extensiones_imagen = ['.jpg', '.jpeg', '.png', '.webp']

            # for division in os.listdir(os.path.isdir(dir_dataset)):
            for division in os.listdir(dir_dataset) if os.path.isdir(dir_dataset) else []:
                dir_division = os.path.join(dir_dataset, division)
                for disease in os.listdir(dir_division) if os.path.isdir(dir_division) else []:
                    dir_disease = os.path.join(dir_division, disease) 

                    # Nuevo directorio segmentado
                    datasetNameSAM = datasetName+"_SAM"
                    dirSAM = os.path.join(HOME, 'datasets', datasetNameSAM, division, disease)
                    os.makedirs(dirSAM, exist_ok=True)
                    cd(dirSAM)

                    for image in os.listdir(dir_disease):
                        for ext in extensiones_imagen:
                            if image.endswith(ext):
                                IMAGE_NAME = image
                                IMAGE_PATH = os.path.join(dir_disease, IMAGE_NAME)

                                #Generar mascaras con el modelo SAM
                                
                                image_bgr = cv2.imread(IMAGE_PATH)
                                image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

                                sam_result = mask_generator.generate(image_rgb)

                                print("SAM_RESULt")
                                print(sam_result)

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

                                print("¡Segmentación automática exitosa! - " + disease)

        path_weight = os.path.join(HOME, 'AppSafeCrops', 'MODELO_SAM') # Directorio para guardar los pesos del modelo SAM

        DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        MODEL_TYPE = "vit_h"

        os.makedirs(path_weight, exist_ok=True) # Crear directorio para guardar los pesos del modelo SAM
        cd(path_weight) # Ingresar a la ruta de weights

        download_sam_weights() # Validar si eya exiten los pesos predeterminados de SAM
        checkpoint = select_checkpoint() # Seleccionar que archivo de checkpoints (pesos) se utilizará para segmentar
        # Cargar el modelo
        sam = sam_model_registry[MODEL_TYPE](checkpoint=checkpoint).to(device=DEVICE).train()

        generar_segmentacion_automatica() # Segmentar dibujando un cuadro delimitador de forma manual

        cd(HOME)
        return 'ok'


        

    # #  #  #  #  #  #  #  #  #  #  #
    # #   Llamada a las funciones   #
    # #  #  #  #  #  #  #  #  #  #  #

    # #install() #Instalar los paquetes necesarios para la segmentación con SAM
    # create_weight_directory() # Validar si existe el directorio para guardar los pesos
    # cd(path_weight) # Ingresar a la ruta de weights
    # download_sam_weights() # Validar si eya exiten los pesos predeterminados de SAM
    # checkpoint = select_checkpoint() # Seleccionar que archivo de checkpoints (pesos) se utilizará para segmentar
    # #create_data_directory() # Validar si existe el directorio para guardar las imágenes de prueba 
    # #cd(path_data) # Ingresar a la ruta de data
    # #download_example_data() # Descargar las imagenes de prueba
    # cd(HOME+"/SafeCrops/imagenes")
    # # Cargar el modelo
    # sam = sam_model_registry[MODEL_TYPE](checkpoint=checkpoint).to(device=DEVICE).train()
    # generar_segmentacion_cuadro_delimitador() # Segmentar dibujando un cuadro delimitador de forma manual
    # #generar_segmentacion_automatica() # Segmentar de forma automática tomando la figura con mayor area dentro de la imagen


