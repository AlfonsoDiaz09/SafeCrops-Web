# Generated by Django 4.2.3 on 2023-08-24 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppSafeCrops', '0021_remove_dataset_estadodataset'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='estadoDataset',
            field=models.CharField(default='Activo', max_length=10, verbose_name='Estado del dataset'),
        ),
    ]
