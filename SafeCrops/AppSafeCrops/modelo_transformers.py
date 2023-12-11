import os
import torch
import numpy as np
from datasets import load_dataset
from datasets import load_metric
from transformers import AutoImageProcessor
from transformers import AutoModelForImageClassification, TrainingArguments, Trainer
from transformers import pipeline
from sklearn.metrics import f1_score, mean_squared_error
from PIL import Image
import requests

from .GLOBAL_VARIABLES import HOME

class Transformer:
    def training_model(nombreTransformer, nombreDataset, epocas, batch_size):

        # HOME = 'D:\SafeCrops-Web\SafeCrops'

        # nombreTransformer = 'WD_Corn_Resized_SAM_Completo'
        # epocas = 15
        # nombreDataset = 'Corn_Resized_SAM_Completo'
        # batch_size = 32



        print("Directorio principal: ", HOME)

        save_model_transformer_dir = os.path.join(HOME, 'modelos', 'transformer')
        save_results_transformer_dir = os.path.join(HOME, 'modelos_resultados', 'transformer')

        os.makedirs(save_model_transformer_dir, exist_ok=True)

        def cd(path):
            try:
                os.chdir(path)
                print("Directorio actual: ", os.getcwd())
            except:
                print("Error al cambiar de directorio")

        cd(save_model_transformer_dir)

        model_checkpoint = "microsoft/swin-tiny-patch4-window7-224" # pre-trained model from which to fine-tune
        num_epoch = epocas # epoch number for train
        datasetName =  str(nombreDataset)
        model_name = nombreTransformer
        batch_size = int(batch_size)

        # # # # # # # # # # # #
        # CARGANDO EL DATASET #
        # # # # # # # # # # # #

        dir_dataset = (HOME+"/datasets/"+datasetName)

        dataset = load_dataset("imagefolder", data_dir=dir_dataset)
        metric = load_metric("accuracy", "f1")

        print(dataset)

        labels = dataset["train"].features["label"].names
        label2id, id2label = dict(), dict()
        for i, label in enumerate(labels):
            label2id[label] = i 
            id2label[i] = label

        # # # # # # #  # # # # #
        # PROCESANDO LOS DATOS #
        # # # # # # #  # # # # #

        image_processor  = AutoImageProcessor.from_pretrained(model_checkpoint)

        from torchvision.transforms import (
            CenterCrop,
            Compose,
            Normalize,
            RandomHorizontalFlip,
            RandomResizedCrop,
            Resize,
            ToTensor,
        )

        normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)
        if "height" in image_processor.size:
            size = (image_processor.size["height"], image_processor.size["width"])
            crop_size = size
            max_size = None
        elif "shortest_edge" in image_processor.size:
            size = image_processor.size["shortest_edge"]
            crop_size = (size, size)
            max_size = image_processor.size.get("longest_edge")

        train_transforms = Compose(
            [
                RandomResizedCrop(crop_size), # Aplica un recorte aleatorio de la imagen y luego la cambia de tamaño a size
                RandomHorizontalFlip(), # Voltea horizontalmente la imagen con una probabilidad del 50%
                ToTensor(), # Convierte la imagen a un tensor de PyTorch
                normalize, # Normaliza el tensor de imagen con mean y std, en donde mean y std son los valores de imagen_mean y image_std de image_processor los cuales se obtienen del modelo pre-entrenado
            ]
        )

        val_transforms = Compose(
            [
                Resize(size), # Cambia el tamaño de la imagen a size
                CenterCrop(crop_size), # Recorta la imagen a una región de tamaño (crop_size) centrada en el centro
                ToTensor(), # Convierte la imagen a un tensor de PyTorch
                normalize, # Normaliza el tensor de imagen con mean y std 
            ]
        )

        def preprocess_train(example_batch):
            """Apply train_transforms across a batch."""
            example_batch["pixel_values"] = [
                train_transforms(image.convert("RGB")) for image in example_batch["image"]
            ]
            return example_batch

        def preprocess_val(example_batch):
            """Apply val_transforms across a batch."""
            example_batch["pixel_values"] = [val_transforms(image.convert("RGB")) for image in example_batch["image"]]
            return example_batch

        # split up training into training + validation
        train_ds = dataset['train']
        val_ds = dataset['validation']

        train_ds.set_transform(preprocess_train)
        val_ds.set_transform(preprocess_val)

        # # # # # # #  # # # # #
        # ENTRENANDO EL MODELO #
        # # # # # # #  # # # # #

        model = AutoModelForImageClassification.from_pretrained(
            model_checkpoint,
            label2id=label2id,
            id2label=id2label,
            ignore_mismatched_sizes = True, # provide this in case you're planning to fine-tune an already fine-tuned checkpoint
        )

        #model_name = model_checkpoint.split("/")[-1]

        args = TrainingArguments(
            f"{model_name}-finetuned",
            remove_unused_columns=False,
            evaluation_strategy = "epoch",
            save_strategy = "epoch",
            learning_rate=5e-5,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_epoch,
            warmup_ratio=0.1,
            logging_steps=10,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            push_to_hub=False,
            weight_decay=0.65,
        )

        metrics_for_epoch = []

        # the compute_metrics function takes a Named Tuple as input:
        # predictions, which are the logits of the model as Numpy arrays,
        # and label_ids, which are the ground-truth labels as Numpy arrays.
        def compute_metrics(eval_pred):
            """Computes accuracy and F1 on a batch of predictions"""
            predictions = np.argmax(eval_pred.predictions, axis=1)
            accuracy = metric.compute(predictions=predictions, references=eval_pred.label_ids)['accuracy']
            f1 = f1_score(eval_pred.label_ids, predictions, average='weighted')  # Puedes ajustar el average según tus necesidades

            result_metrics = {"accuracy": accuracy, "f1": f1}
            print("METRIc_FA: ", result_metrics)
            metrics_for_epoch.append(result_metrics)
            return result_metrics

        def collate_fn(examples):
            pixel_values = torch.stack([example["pixel_values"] for example in examples])
            labels = torch.tensor([example["label"] for example in examples])
            return {"pixel_values": pixel_values, "labels": labels}

        trainer = Trainer(
            model,
            args,
            train_dataset=train_ds,
            eval_dataset=val_ds,
            tokenizer=image_processor,
            compute_metrics=compute_metrics,
            data_collator=collate_fn,
        )

        train_results = trainer.train()
        print("TRAIN_RESULTS: ", train_results)
        # rest is optional but nice to have
        trainer.save_model()
        trainer.log_metrics("train", train_results.metrics)
        trainer.save_metrics("train", train_results.metrics)
        trainer.save_state()

        metrics = trainer.evaluate()
        print("METRICS: ", metrics)
        # some nice to haves:
        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)

        return metrics, metrics_for_epoch

    # Inferencia
    def prediction_model():

        url = HOME+"/datasets/Corn_TEST/"
        modelo = 'MT_Corn_SAM_15e_8bs'
        dir_modelo = os.path.join(HOME, 'modelos', 'transformer', modelo+'-finetuned')
        errores_cuadraticos = []
        for division in os.listdir(url):
            if division == "test":
                for disease in os.listdir(url+division):
                    for img in os.listdir(url+division+"/"+disease):
                        img = url+division+"/"+disease+"/"+img
                        print("\n"+img)
                        #image = Image.open(requests.get(url, stream=True).raw)
                        image = Image.open(img)

                        repo_name = dir_modelo

                        # image_processor = AutoImageProcessor.from_pretrained(repo_name)
                        # model = AutoModelForImageClassification.from_pretrained(repo_name)

                        # # prepare image for the model
                        # encoding = image_processor(image.convert("RGB"), return_tensors="pt")
                        # print("Encoding: ", encoding.pixel_values.shape)

                        # # forward pass
                        # with torch.no_grad():
                        #     outputs = model(**encoding)
                        #     logits = outputs.logits

                        # predicted_class_idx = logits.argmax(-1).item()
                        # print("Predicted class: ", model.config.id2label[predicted_class_idx])

                        pipe = pipeline("image-classification", repo_name)
                        prediction = pipe(image)[0]['label']
                        print("Prediction: ", prediction)
                        score = pipe(image)[0]['score']
                        print("Score: ", score)
                        

                        #Error cuadrado medio
                        y_true = [0.9730]
                        y_pred = [score]

                        mse = round(mean_squared_error(y_true, y_pred), 3)
                        print(f"Error cuadrático medio: {mse}\n")
                        
                        errores_cuadraticos.append(mse)
        promedio_MSE = round(sum(errores_cuadraticos)/len(errores_cuadraticos), 3)
        print("Promedio de error cuadrático médio: ", promedio_MSE)


    # EJECUTAR FUCIONES #

    #training_model()
    #prediction_model()



