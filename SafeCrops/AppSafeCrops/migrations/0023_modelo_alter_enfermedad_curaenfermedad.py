# Generated by Django 4.2.3 on 2023-09-01 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSafeCrops', '0022_dataset_estadodataset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id_Modelo', models.AutoField(primary_key=True, serialize=False)),
                ('nombreModelo', models.CharField(max_length=45, unique=True, verbose_name='Nombre del Modelo')),
                ('pesosModelo', models.FileField(upload_to='modelos/', verbose_name='Ruta de los Pesos')),
                ('tipoModelo', models.CharField(max_length=45, verbose_name='Tipo de Modelo')),
                ('estadoModelo', models.CharField(default='Activo', max_length=10, verbose_name='Estado del modelo')),
            ],
        ),
        migrations.AlterField(
            model_name='enfermedad',
            name='curaEnfermedad',
            field=models.TextField(max_length=200, verbose_name='Tratamiento de la enfermedad'),
        ),
    ]
