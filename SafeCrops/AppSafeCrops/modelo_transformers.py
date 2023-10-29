import os
import torch
import numpy as np
from datasets import load_dataset
from datasets import load_metric
from transformers import AutoImageProcessor
from transformers import AutoModelForImageClassification, TrainingArguments, Trainer
from transformers import pipeline
from PIL import Image
import requests

class Transformer:
    
    def training_model(nombreTransformer, nombreDataset, epocas, batch_size):

        HOME = os.getcwd() # Directorio principal
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
        metric = load_metric("accuracy")

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
                RandomResizedCrop(crop_size),
                RandomHorizontalFlip(),
                ToTensor(),
                normalize,
            ]
        )

        val_transforms = Compose(
            [
                Resize(size),
                CenterCrop(crop_size),
                ToTensor(),
                normalize,
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
            f"{model_name}-finetuned-transformer",
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
        )

        # the compute_metrics function takes a Named Tuple as input:
        # predictions, which are the logits of the model as Numpy arrays,
        # and label_ids, which are the ground-truth labels as Numpy arrays.
        def compute_metrics(eval_pred):
            """Computes accuracy on a batch of predictions"""
            predictions = np.argmax(eval_pred.predictions, axis=1)
            return metric.compute(predictions=predictions, references=eval_pred.label_ids)

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
        # rest is optional but nice to have
        trainer.save_model()
        trainer.log_metrics("train", train_results.metrics)
        trainer.save_metrics("train", train_results.metrics)
        trainer.save_state()

        metrics = trainer.evaluate()
        # some nice to haves:
        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)

        cd(HOME)

    # Inferencia
    def prediction_model():
        url = HOME+"/SafeCrops/datasets/Corn/validate/Corn_NLS/nls_550.jpg"
        print(url)
        #image = Image.open(requests.get(url, stream=True).raw)
        image = Image.open(url)

        repo_name = HOME+"/swin-tiny-patch4-window7-224-finetuned/"

        image_processor = AutoImageProcessor.from_pretrained(repo_name)
        model = AutoModelForImageClassification.from_pretrained(repo_name)

        # prepare image for the model
        encoding = image_processor(image.convert("RGB"), return_tensors="pt")
        print("Encoding: ", encoding.pixel_values.shape)

        # forward pass
        with torch.no_grad():
            outputs = model(**encoding)
            logits = outputs.logits

        predicted_class_idx = logits.argmax(-1).item()
        print("Predicted class: ", model.config.id2label[predicted_class_idx])

        pipe = pipeline("image-classification", repo_name)
        print(pipe(image)[0])
        print(pipe(image)[1])
        print(pipe(image)[2])



    # EJECUTAR FUCIONES #

    #training_model()
    #prediction_model()



