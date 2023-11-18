# Generated by Django 4.2.3 on 2023-11-17 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppSafeCrops', '0037_modelo_transformer_f1score_transformer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelo_yolov5',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='yolov5User', to=settings.AUTH_USER_MODEL, verbose_name='ID_Usuario'),
        ),
        migrations.AddField(
            model_name='modelo_yolov7',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='yolov7User', to=settings.AUTH_USER_MODEL, verbose_name='ID_Usuario'),
        ),
    ]