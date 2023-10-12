# Generated by Django 4.2.3 on 2023-10-08 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSafeCrops', '0023_modelo_alter_enfermedad_curaenfermedad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modelo_YOLOv7',
            fields=[
                ('id_Modelo_y7', models.AutoField(primary_key=True, serialize=False)),
                ('nombreModelo_y7', models.CharField(max_length=45, unique=True, verbose_name='Nombre del Modelo')),
                ('pesosModelo_y7', models.FileField(help_text='Selecciona un archivo de pesos correcto', upload_to='modelos/yolov7/', verbose_name='Ruta de los Pesos')),
                ('epocas_y7', models.IntegerField(help_text='Selecciona un valor entre 1 y 6', verbose_name='Número de épocas')),
                ('batch_size_y7', models.IntegerField(help_text='Selecciona un valor mayor a 2', verbose_name='Batch Size')),
            ],
        ),
        migrations.DeleteModel(
            name='Modelo',
        ),
    ]
