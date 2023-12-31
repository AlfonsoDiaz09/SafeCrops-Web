from typing import Any, Dict
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Administrador, Experto, Tester, Enfermedad, Dataset, Cultivo, Modelo_YOLOv5, Modelo_YOLOv7, Modelo_Transformer

'''
Se crea los formularios a partir de los campos que se encuentran en los modelos o creando 
nuevos campos haciendo uso de los widgets de django
'''

Batch_Size = (
    ('', '------ SELECCIONE ------'),
    (512, 512),
    (256, 256),
    (128, 128),
    (64, 64),
    (32, 32),
    (16, 16),
    (8, 8),
    (4, 4),
    (2, 2),
    (1, 1),
)

estadoDataset = (
    ('Todos', 'Todos'),
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo'),
)

class TempUsuario(forms.ModelChoiceField): # Se crea una clase para el campo de tipo ModelChoiceField
    def label_from_instance(self, obj): # Se define el método label_from_instance
        return str(obj.id)+" - "+str(obj.username) # Se retorna el valor que se va a mostrar en el campo


class AdministradorForm(forms.ModelForm, forms.Form):  # Formulario para el modelo Administrador
    #user = TempUsuario(queryset=User.objects.all().order_by('-id'), label=None, widget=forms.Select(attrs={'class':'form-select'})) # Se crea un campo de tipo ModelChoiceField

    class Meta: # Se define la clase Meta
        model = Administrador # Se define el modelo
        fields = ['id_Administrador', 'nombre', 'apellidoP', 'apellidoM', 'fechaNac', 'correo', 'imagen', 'userType'] # Se definen los campos que se van a mostrar en el formulario


class ExpertoForm(forms.ModelForm, forms.Form): # Formulario para el modelo Experto
    #user = TempUsuario(queryset=User.objects.all().order_by('-id'), label=None, widget=forms.Select(attrs={'class':'form-select'})) # Se crea un campo de tipo ModelChoiceField

    class Meta: # Se define la clase Meta 
        model = Experto # Se define el modelo
        fields = ['nombre', 'apellidoP', 'apellidoM', 'fechaNac', 'correo', 'institucionPerteneciente', 'imagen', 'userType']  # Se definen los campos que se van a mostrar en el formulario


class TesterForm(forms.ModelForm): # Formulario para el modelo Tester
    #user = TempUsuario(queryset=User.objects.all().order_by('-id'), label=None, widget=forms.Select(attrs={'class':'form-select'})) # Se crea un campo de tipo ModelChoiceField

    class Meta: # Se define la clase Meta
        model = Tester # Se define el modelo
        fields = ['nombre', 'apellidoP', 'apellidoM', 'fechaNac', 'correo', 'imagen', 'userType'] # Se definen los campos que se van a mostrar en el formulario


class UsuarioForm(UserCreationForm, forms.ModelForm): # Formulario para el modelo Usuario
    password1: forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'})) # Se define el campo password1
    password2: forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'})) # Se define el campo password2
   
    class Meta: # Se define la clase Meta
        model = User # Se define el modelo
        fields = ['username', 'password1', 'password2'] # Se definen los campos que se van a mostrar en el formulario


class ResetPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'autocomplete': 'on',
        'autofocus': True
    }))

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'autocomplete': 'off',
        'autofocus': True
    }))

    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'autocomplete': 'off'
    }))

class EnfermedadForm(forms.ModelForm):
    cultivoEnfermedad = forms.ModelChoiceField(queryset=Cultivo.objects.all().order_by('-id_Cultivo'), label="Cultivo en el que se presenta", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    
    class Meta:
        model = Enfermedad
        fields = '__all__'

class DatasetForm(forms.ModelForm):
    ruta = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['zip'])])
    tipoDataset = forms.ModelChoiceField(queryset=Cultivo.objects.all().order_by('-id_Cultivo'), label="Tipo de Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    class Meta:
        model = Dataset
        fields = ['nombreDataset', 'tipoDataset', 'ruta', 'segmentacion_SAM', 'homogenizacion_YIQ', 'formatoImg']

class CultivoForm(forms.ModelForm):
    class Meta:
        model = Cultivo
        fields = '__all__'

class Modelo_YOLOv5_Form(forms.ModelForm):
    datasetModelo_y5 = forms.ModelChoiceField(queryset=Dataset.objects.all().order_by('-id_Dataset'), label="Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    batch_size_y5 = forms.ChoiceField(choices=Batch_Size, widget=forms.Select(attrs={'class':'form-select formulario__select'}))
    class Meta:
        model = Modelo_YOLOv5
        fields = ['nombreModelo_y5', 'datasetModelo_y5', 'pesosModelo_y5', 'epocas_y5', 'batch_size_y5']

class Modelo_YOLOv7_Form(forms.ModelForm):
    datasetModelo_y7 = forms.ModelChoiceField(queryset=Dataset.objects.all().order_by('-id_Dataset'), label="Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    batch_size_y7 = forms.ChoiceField(choices=Batch_Size, widget=forms.Select(attrs={'class':'form-select formulario__select'}))
    class Meta:
        model = Modelo_YOLOv7
        fields = ['nombreModelo_y7', 'datasetModelo_y7', 'pesosModelo_y7', 'epocas_y7', 'batch_size_y7']

class Modelo_Transformer_Form(forms.ModelForm):
    datasetModelo_transformer = forms.ModelChoiceField(queryset=Dataset.objects.all().order_by('-id_Dataset'), label="Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    batch_size_transformer = forms.ChoiceField(choices=Batch_Size, widget=forms.Select(attrs={'class':'form-select formulario__select'}))

    class Meta:
        model = Modelo_Transformer
        fields = ['nombreModelo_transformer', 'datasetModelo_transformer', 'pesosModelo_transformer', 'epocas_transformer', 'batch_size_transformer']


class TempDataset(forms.ModelChoiceField): # Se crea una clase para el campo de tipo ModelChoiceField
    def label_from_instance(self, obj): # Se define el método label_from_instance
        return obj.nombreDataset # Se retorna el valor que se va a mostrar en el campo

class ReporteForm(forms.Form):
    nombreDataset = TempDataset(queryset=Dataset.objects.all(), label="Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField

    class Meta:
        fields = ['nombreDataset']

class ListaDatasetsForm(forms.Form):
    estadoDataset = forms.ChoiceField(choices=estadoDataset, label="Estado de Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}))

    class Meta:
        fields = ['estadoDataset']

class HomogeneizacionForm(forms.Form):
    nombreDataset = TempDataset(queryset=Dataset.objects.all(), label="Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField

    class Meta:
        fields = ['nombreDataset']

class TempTransformer(forms.ModelChoiceField): # Se crea una clase para el campo de tipo ModelChoiceField
    def label_from_instance(self, obj): # Se define el método label_from_instance
        return obj.nombreModelo_transformer # Se retorna el valor que se va a mostrar en el campo

class TempYolov5(forms.ModelChoiceField): # Se crea una clase para el campo de tipo ModelChoiceField
    def label_from_instance(self, obj): # Se define el método label_from_instance
        return obj.nombreModelo_y5 # Se retorna el valor que se va a mostrar en el campo

class TempYolov7(forms.ModelChoiceField): # Se crea una clase para el campo de tipo ModelChoiceField
    def label_from_instance(self, obj): # Se define el método label_from_instance
        return obj.nombreModelo_y7 # Se retorna el valor que se va a mostrar en el campo

class EvaluacionModelosForm(forms.Form):
    modelo_Transformer = TempTransformer(queryset=Modelo_Transformer.objects.all().order_by('-id_Modelo_transformer'), label="Modelo Transformer", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    # modelo_YOLOv5 = TempYolov5(queryset=Modelo_YOLOv5.objects.all().order_by('-id_Modelo_y5'), label="Modelo YOLOv5", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    # modelo_YOLOv7 = TempYolov7(queryset=Modelo_YOLOv7.objects.all().order_by('-id_Modelo_y7'), label="Modelo YOLOv7", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField
    nombreDataset = TempDataset(queryset=Dataset.objects.all(), label="Dataset", widget=forms.Select(attrs={'class':'form-select formulario__select'}), empty_label='------ SELECCIONE ------') # Se crea un campo de tipo ModelChoiceField

    class Meta:
        fields = ['modelo_Transformer','nombreDataset']