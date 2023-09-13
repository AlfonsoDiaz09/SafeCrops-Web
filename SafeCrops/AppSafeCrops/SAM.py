# https://github.com/alexFocus92/youtube_projects/blob/main/how_to_segment_anything_with_sam.ipynb


import os
import sys
import pip
import subprocess



HOME = os.getcwd() # Directorio actual

# Función para mostrar el directorio actual
def current_directory():
    print("HOME:", HOME)

# Función para instalar paquetes con try except

def install():
    try:
        subprocess.call([sys.executable, "-m", ".\DJSafeCrops\Scripts"+"/activate"]) #Activar entorno virtual
        subprocess.call([sys.executable, "-m", "pip", "install", "git+https://github.com/facebookresearch/segment-anything.git"]) #Instalar numpy con pip
        subprocess.call([sys.executable, "-m", "pip", "install", "numpy"]) #Instalar numpy con pip
        subprocess.call([sys.executable, "-m", "pip", "install", "wget"])
        subprocess.call([sys.executable, "-m", "pip", "install", "torch"])
        subprocess.call([sys.executable, "-m", "pip", "install", "torchvision"])
        subprocess.call([sys.executable, "-m", "pip", "install", "opencv-python==4.7.0.72"])
        subprocess.call([sys.executable, "-m", "pip", "install", "matplotlib"])
        subprocess.call([sys.executable, "-m", "pip", "install", "supervision"])
    except:
        print("Error al instalar el paquete")


# Función para crear directorios con try except
def create_directory_weight(path_weight):
    try:
        os.mkdir(HOME+"/weights")
    except:
        print("Error al crear el directorio")

# Función para cambiar de directorio de pesos con try except
def cd(path):
    try:
        os.chdir(path)
        
    except:
        print("Error al cambiar de directorio")

# Función para crear directorio de datos con try except
def create_directory_data(path_data):
    try:
        os.mkdir(HOME+"/data")
    except:
        print("Error al crear el directorio")

# Función para descargar los datos de ejemplo
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


# Llamada a las funciones
path_weight = HOME+"/weights"
path_data = HOME+"/data"

current_directory()
install()
import wget

if not os.path.exists(path_weight):
    create_directory_weight(path_weight)
else:
    print("El directorio ya existe")

cd(path_weight)
print("Directorio actual:", os.getcwd())

if not os.path.exists("sam_vit_h_4b8939.pth"):
    wget.download('https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth')
else:
    print("El archivo ya se encuentra descargado")


if os.path.exists("fine_tuned_sam.pth"):
    CHECKPOINT_PATH = os.path.join(HOME, "weights", "fine_tuned_sam.pth")
else:
    CHECKPOINT_PATH = os.path.join(HOME, "weights", "sam_vit_h_4b8939.pth")

print(CHECKPOINT_PATH, "; exist:", os.path.isfile(CHECKPOINT_PATH))

if not os.path.exists(path_data):
    create_directory_data(path_data)
else:
    print("El directorio ya existe")

cd(path_data)
print("Directorio actual:", os.getcwd())

download_example_data()

# Cargar el modelo
import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", DEVICE)
MODEL_TYPE = "vit_h"

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH).to(device=DEVICE)

#Generar máscaras automáticamente
# mask_generator = SamAutomaticMaskGenerator(sam)

# IMAGE_NAME = "dog.jpeg"
# IMAGE_PATH = os.path.join(HOME, "data", IMAGE_NAME)

#Generar mascaras con el modelo SAM
# import cv2
# import supervision as sv
# import numpy as np

# image_bgr = cv2.imread(IMAGE_PATH)
# print(image_bgr)
# image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

# sam_result = mask_generator.generate(image_rgb)

# print("RESULTS: ",sam_result[0].keys())

# Visualizar los resultados con supervision
# mask_annotator = sv.MaskAnnotator()

# detections = sv.Detections.from_sam(sam_result = sam_result)

# annotated_image = mask_annotator.annotate(scene = image_bgr.copy(), detections = detections)

# sv.plot_images_grid(
#     images = [image_bgr, annotated_image],
#     grid_size = (1, 2),
#     titles = ["Original", "Segmentation"]
# )

# Interacción con los resultados de la segmentación
# masks = [
#     mask['segmentation'] for mask in sorted(sam_result, key=lambda x: x['area'], reverse=True)
# ]

# sv.plot_images_grid(
#     images = masks,
#     grid_size = (2, int(len(masks)/2)),
#     size = (16, 16)
# )

# Generar segmentación con cuadro delimitador
import cv2
import supervision as sv
import numpy as np


mask_predictor = SamPredictor(sam)

IMAGE_NAME = "planta.jpg"
IMAGE_PATH = os.path.join(HOME, "data", IMAGE_NAME)

# Draw box
import base64 # Codificar imagen en base64 para mostrarla en el notebook de Jupyter Lab o Jupyter Notebook

def encode_image(filepath):
    with open(filepath, "rb") as f:
        image_bytes = f.read()
    encoded = str(base64.b64encode(image_bytes), 'utf-8')
    return "data:image/jpeg;base64," + encoded

# from jupyter_bbox_widget import BboxWidget

# widget = BboxWidget()
# widget.image = encode_image(IMAGE_PATH)
# widget
# widget.bboxes

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
print("IMAGEEEEN ",imagen)
coordenadas = drawing_bbox(imagen)

print("Coordenadas del cuadro delimitador:")
print(coordenadas)

box = np.array([
    coordenadas[0][0],
    coordenadas[0][1],
    coordenadas[1][0],
    coordenadas[1][1]
])

image_bgr = cv2.imread(IMAGE_PATH)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

mask_predictor.set_image(image_rgb)

masks, scores, logits = mask_predictor.predict(
    box=box,
    multimask_output=True
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