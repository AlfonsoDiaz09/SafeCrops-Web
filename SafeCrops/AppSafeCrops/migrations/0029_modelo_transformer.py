# Generated by Django 4.2.3 on 2023-10-27 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSafeCrops', '0028_alter_modelo_yolov7_batch_size_y7_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modelo_Transformer',
            fields=[
                ('id_Modelo_transformer', models.AutoField(primary_key=True, serialize=False)),
                ('nombreModelo_transformer', models.CharField(max_length=45, unique=True, verbose_name='Nombre del Modelo')),
                ('pesosModelo_transformer', models.FileField(upload_to='weights/Transformer/', verbose_name='Ruta de Pesos')),
                ('epocas_transformer', models.IntegerField(verbose_name='Número de épocas')),
                ('batch_size_transformer', models.IntegerField(verbose_name='Batch Size')),
                ('accuracy_transformer', models.FloatField(blank=True, null=True, verbose_name='Accuracy')),
                ('loss_transformer', models.FloatField(blank=True, null=True, verbose_name='Loss')),
                ('ruta_resultados_transformer', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ruta de resultados')),
            ],
        ),
    ]
