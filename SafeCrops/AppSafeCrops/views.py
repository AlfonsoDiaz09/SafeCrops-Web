
from base64 import urlsafe_b64decode
import os
import shutil
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from .models import Administrador, Experto, Tester, Enfermedad, Dataset, Usuario, Cultivo, Modelo_YOLOv7, Modelo_Transformer
from .forms import AdministradorForm, ExpertoForm, TesterForm, UsuarioForm, ResetPasswordForm, ChangePasswordForm, EnfermedadForm, DatasetForm, CultivoForm, Modelo_YOLOv7_Form, Modelo_Transformer_Form
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from .zip import Zip
from .modelo_transformers import Transformer
#from .MODELO_YOLOv7.train import YOLOv7
import subprocess
import sys
from .GLOBAL_VARIABLES import cd, HOME, query_ruta_dataset
import mysql.connector

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import uuid

# Create your views here.


#*****************************************************************************************************#
#**********               VALIDACIÓN DE TIPO DE USUARIO PARA PANEL PRINCIPAL                **********#
#*****************************************************************************************************#

def validation(request):

    administradores = Administrador.objects.all()
    expertos = Experto.objects.all()
    testers = Tester.objects.all()

    idAdministrador = []
    idExperto = []
    idTester = []

    for administrador in administradores:
        idAdministrador.append(administrador.user_id)
    for experto in expertos:
        idExperto.append(experto.user_id)
    for tester in testers:
        idTester.append(tester.user_id)

    if request.user.is_authenticated:
        if request.user.id in idAdministrador or request.user.is_superuser:
            return HttpResponseRedirect('/Panel_administrador')
        elif request.user.id in idExperto:
            return HttpResponseRedirect('/Panel_experto')
        elif request.user.id in idTester:
            return HttpResponseRedirect('/Panel_tester')

    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                if request.user.id in idAdministrador or request.user.is_superuser:
                    return HttpResponseRedirect('/Panel_administrador')
                elif request.user.id in idExperto:
                    return HttpResponseRedirect('/Panel_experto')
                elif request.user.id in idTester:
                    return HttpResponseRedirect('/Panel_tester')
                else:
                    return HttpResponseRedirect('/login')
            else:
                return redirect('login/')
        else:
            fm = AuthenticationForm()
            messages.info(request, 'Usuario o contraseña incorrectos. Intentelo de nuevo.')
    else:
        fm = AuthenticationForm()
        
    return render(request, 'registration/login.html', {'direccion' : 'Login','form': fm})


#*****************************************************************************************************#
#**********                         INGRESAR EMAIL PARA ENVIAR TOKEN                        **********#
#*****************************************************************************************************#

def ResetPassword(request):
    form_class = ResetPasswordForm(request.GET or None)
    return render(request, 'registration/password_reset.html', {'direccion' : 'Restablecer contraseña', 'form': form_class})


#*****************************************************************************************************#
#**********              ENVIAR EMAIL CON TOKEN DE RECUPERACIÓN DE CONTRASEÑA               **********#
#*****************************************************************************************************#

def sendEmail(request):
    mail = request.GET.get('email')
    queryEmailAdmin = Administrador.objects.all()
    queryEmailExperto = Experto.objects.all()
    queryEmailTester = Tester.objects.all()
    
    bandera = False
    
    for user in queryEmailAdmin:
        if mail == user.correo:
            print("Enviar correo a", mail)
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            print("Usuario ", user)
            print("Prueba ", user.nombre)
            print("Token ", user.token)
            user.save()
            #obtener una imagen que sera enviada en el correo
            user_admin = User.objects.get(id=user.user_id)
            context={
                'mail':mail,
                'imagen_profile': user.imagen,
                'nombre':user.nombre,
                'user':user_admin,
                'link_resetpwd': 'http://{}/change_password{}'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
                }
            template = get_template('registration/send_email_reset_pwd.html')
            content = render_to_string('registration/send_email_reset_pwd.html', context)
            
            email = EmailMultiAlternatives(
                'Recuperación de contraseña Safe Crops',
                'SafeCrops',
                settings.EMAIL_HOST_USER,#Origen
                [mail],#Destinatarios

            )
            email.attach_alternative(content,'text/html')
            email.send()
            messages.success(request, f'Correo enviado correctamente')
            bandera = True

    for user in queryEmailExperto:
        if mail == user.correo:
            print("Enviar correo a", mail)
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            print("Usuario ", user)
            print("Prueba ", user.nombre)
            print("Token ", user.token)
            user.save()
            user_experto = User.objects.get(id=user.user_id)
            context={
                'mail':mail, 
                'nombre':user.nombre, 
                'user':user_experto,
                'link_resetpwd': 'http://{}/change_password{}'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
                }
            template = get_template('registration/send_email_reset_pwd.html')
            content = render_to_string('registration/send_email_reset_pwd.html', context)
            
            email = EmailMultiAlternatives(
                'Recuperación de contraseña Safe Crops',
                'SafeCrops',
                settings.EMAIL_HOST_USER,#Origen
                [mail],#Destinatarios

            )
            email.attach_alternative(content,'text/html')
            email.send()
            messages.success(request, f'Correo enviado correctamente')
            bandera = True

    for user in queryEmailTester:
        if mail == user.correo:
            print("Enviar correo a", mail)
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            print("Usuario ", user)
            print("Prueba ", user.nombre)
            print("Token ", user.token)
            user.save()
            user_tester = User.objects.get(id=user.user_id)
            context={
                'mail':mail, 
                'nombre':user.nombre,
                'user':user_tester,
                'link_resetpwd': 'http://{}/change_password{}'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
                }
            template = get_template('registration/send_email_reset_pwd.html')
            content = render_to_string('registration/send_email_reset_pwd.html', context)
            
            email = EmailMultiAlternatives(
                'Recuperación de contraseña Safe Crops',
                'SafeCrops',
                settings.EMAIL_HOST_USER,#Origen
                [mail],#Destinatarios

            )
            email.attach_alternative(content,'text/html')
            email.send()
            messages.success(request, f'Correo enviado correctamente')
            bandera = True

    if bandera == False:
        messages.error(request, f'El correo {mail} no existe en la base de datos')
    return redirect('passwordReset')


#*****************************************************************************************************#
#**********                             GENERAR NUEVA CONTRASEÑA                            **********#
#*****************************************************************************************************#

def ChangePassword(request, token):
    form_class = ChangePasswordForm(request.POST or None)
    bandera = False
    user = None
    
    if Administrador.objects.filter(token=token).exists():
        user = Administrador.objects.get(token=token)
        bandera = True
    if Experto.objects.filter(token=token).exists():
        user = Experto.objects.get(token=token)
        bandera = True
    if Tester.objects.filter(token=token).exists():
        user = Tester.objects.get(token=token)
        bandera = True
    
    if bandera == False:
        messages.error(request, f'El token no existe en la base de datos')
    elif bandera == True:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                print("Formulario valido ", user.user_id)
                user = User.objects.get(id=user.user_id)
                user.set_password(form.cleaned_data['password'])
                user.save()

                messages.success(request, f'Contraseña cambiada correctamente')
                return redirect('login/')
            else:
                form = ChangePasswordForm()
        return render(request, 'registration/change_pwd.html', {'direccion' : 'Restablecer contraseña / Nueva contraseña', 'form': form_class})


def user_profile(request):
    return render(request, 'usuarios/tester/inicioT.html')


#*****************************************************************************************************#
#**********                      REGISTRO DE USUARIOS SIN SESIÓN ACTIVA                     **********#
#*****************************************************************************************************#

def registerUsers(request):
    administradores = Administrador.objects.all()
    expertos = Experto.objects.all()
    testers = Tester.objects.all()

    idAdministrador = []
    idExperto = []
    idTester = []

    for administrador in administradores:
        idAdministrador.append(administrador.user_id)
    for experto in expertos:
        idExperto.append(experto.user_id)
    for tester in testers:
        idTester.append(tester.user_id)

    if request.user.is_authenticated:
        if request.user.id in idAdministrador or request.user.is_superuser:
            return HttpResponseRedirect('/Panel_administrador')
        elif request.user.id in idExperto:
            return HttpResponseRedirect('/Panel_experto')
        elif request.user.id in idTester:
            return HttpResponseRedirect('/Panel_tester')
        
    return render(request, 'registration/register.html', {'direccion': 'Registro'})

def registerAdmin(request): #función para crear un nuevo administrador
    administradores = Administrador.objects.all()
    expertos = Experto.objects.all()
    testers = Tester.objects.all()

    idAdministrador = []
    idExperto = []
    idTester = []

    for administrador in administradores:
        idAdministrador.append(administrador.user_id)
    for experto in expertos:
        idExperto.append(experto.user_id)
    for tester in testers:
        idTester.append(tester.user_id)

    if request.user.is_authenticated:
        if request.user.id in idAdministrador or request.user.is_superuser:
            return HttpResponseRedirect('/Panel_administrador')
        elif request.user.id in idExperto:
            return HttpResponseRedirect('/Panel_experto')
        elif request.user.id in idTester:
            return HttpResponseRedirect('/Panel_tester')

    text = "Registro / Administrador"
    context = {'direccion': text}
    if request.method == 'POST':
        formularioUsuario = UsuarioForm(request.POST or None)
        formularioAdministrador = AdministradorForm(request.POST or None, request.FILES or None)
        # Se valida que los formularios sean válidos
        if formularioUsuario.is_valid() and formularioAdministrador.is_valid():
            # Se crean variables para los datos necesarios para realizar las operaciones siguientes
            id_administrador = formularioAdministrador.cleaned_data['id_Administrador']
            nombre = formularioAdministrador.cleaned_data['nombre']
            usuario = formularioUsuario.cleaned_data['username']

            # Se guardan los formularios de usuario y administrador
            formularioUsuario.save()
            formularioAdministrador.save()

            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
            
            # Se crea una sentencia para obtener el id del último usuario registrado
            last_id = conection.cursor()
            last_id.execute("""SELECT id FROM auth_user ORDER BY id DESC LIMIT 1""")
            id_usuario = last_id.fetchone()
            id_usuario = int(id_usuario[0])
            last_id.close()

            # Se crea una sentencia para actualizar el id del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE appsafecrops_administrador set user_id = %s WHERE id_Administrador = %s""", (id_usuario, id_administrador)) #se actualiza la ruta del dataset
            conection.commit()
            myquery.close()

            # Se envia un mensaje de registro exitoso al template
            messages.success(request, f'Administrador(a) {nombre} con usuario {usuario} creado correctamente')
            
            # Se redirecciona a la página de la lista de administradores
            return redirect('administradores')
    else: # Si no se ha enviado el formulario
        formularioUsuario = UsuarioForm()
        formularioAdministrador = AdministradorForm()
        #formularioUsuario = UsuarioForm(instance=request.user)
        #formularioAdministrador = AdministradorForm(instance=request.user.administradorUser)
    return render(request, 'registration/registerAdmin.html', {'direccion' : 'Registro / Administrador','formularioUsuario': formularioUsuario, 'formularioAdministrador': formularioAdministrador})

def registerExperto(request): #función para crear un nuevo experto
    administradores = Administrador.objects.all()
    expertos = Experto.objects.all()
    testers = Tester.objects.all()

    idAdministrador = []
    idExperto = []
    idTester = []

    for administrador in administradores:
        idAdministrador.append(administrador.user_id)
    for experto in expertos:
        idExperto.append(experto.user_id)
    for tester in testers:
        idTester.append(tester.user_id)

    if request.user.is_authenticated:
        if request.user.id in idAdministrador or request.user.is_superuser:
            return HttpResponseRedirect('/Panel_administrador')
        elif request.user.id in idExperto:
            return HttpResponseRedirect('/Panel_experto')
        elif request.user.id in idTester:
            return HttpResponseRedirect('/Panel_tester')

    if request.method == 'POST':
        formularioUsuario = UsuarioForm(request.POST or None)
        formularioExperto = ExpertoForm(request.POST or None, request.FILES or None)
        # Se valida que los formularios sean válidos
        if formularioUsuario.is_valid() and formularioExperto.is_valid():
            # Se crean variables para los datos necesarios para realizar las operaciones siguientes
            nombre = formularioExperto.cleaned_data['nombre']
            usuario = formularioUsuario.cleaned_data['username']

            # Se guardan los formularios de usuario y administrador
            formularioUsuario.save()
            formularioExperto.save()

            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
            
            # Se crea una sentencia para obtener el id del último usuario registrado
            last_id = conection.cursor()
            last_id.execute("""SELECT id FROM auth_user ORDER BY id DESC LIMIT 1""")
            id_usuario = last_id.fetchone()
            id_usuario = int(id_usuario[0])
            last_id.close()

            last_id_experto = conection.cursor()
            last_id_experto.execute("""SELECT id_Experto FROM appsafecrops_experto ORDER BY id_Experto DESC LIMIT 1""")
            id_experto = last_id_experto.fetchone()
            id_experto = int(id_experto[0])
            last_id_experto.close()

            # Se crea una sentencia para actualizar el id del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE appsafecrops_experto set user_id = %s WHERE id_Experto = %s""", (id_usuario, id_experto)) #se actualiza la ruta del dataset
            conection.commit()
            myquery.close()

            # Se envia un mensaje de registro exitoso al template
            messages.success(request, f'Experto(a) {nombre} con usuario {usuario} creado correctamente')
            
            # Se redirecciona a la página de la lista de administradores
            return redirect('expertos')
    else: # Si no se ha enviado el formulario
        formularioUsuario = UsuarioForm()
        formularioExperto = ExpertoForm()
    return render(request, 'registration/registerExperto.html', {'direccion' : 'Registro / Experto', 'formularioUsuario': formularioUsuario, 'formularioExperto': formularioExperto})


# función para cerrar sesión
def salir(request):
    logout(request)
    return redirect('login/')

#función para redireccionar a la página de inicio principal
def inicio(request):
    administradores = Administrador.objects.all()
    expertos = Experto.objects.all()
    testers = Tester.objects.all()

    idAdministrador = []
    idExperto = []
    idTester = []

    for administrador in administradores:
        idAdministrador.append(administrador.user_id)
    for experto in expertos:
        idExperto.append(experto.user_id)
    for tester in testers:
        idTester.append(tester.user_id)

    if request.user.is_authenticated:
        if request.user.id in idAdministrador or request.user.is_superuser:
            return HttpResponseRedirect('/Panel_administrador')
        elif request.user.id in idExperto:
            return HttpResponseRedirect('/Panel_experto')
        elif request.user.id in idTester:
            return HttpResponseRedirect('/Panel_tester')
        
    return render(request, 'paginas/inicio.html', {'direccion' : 'Inicio'})

#función para traer los datos del usuario logueado
def perfil(request):
    #obtener el id del usuario logueado
    id = request.user.id
    #obtener el usuario logueado
    usuario = User.objects.get(id=id)
    #obtener el administrador logueado
    administrador = Administrador.objects.get(user_id=usuario.id)
    #obtener el nombre del administrador logueado
    nombre = administrador.nombre
    #obtener el apellido del administrador logueado
    apellidoP = administrador.apellidoP
    #obtener el correo del administrador logueado
    correo = administrador.correo
    #obtener la foto del administrador logueado
    imagen = '/imagenes/'+str(administrador.imagen)

    context = {
               'nombre': nombre, 
               'apellido': apellidoP, 
               'correo': correo, 
               'imagen': imagen
              }
    return context

#función para contar los usuarios registrados y retornarlos
def contarUsuarios():
    num_usuarios = User.objects.all().count()
    return num_usuarios

#función para contar los cultivos registrados y retornarlos
def contarCultivos():
    num_cultivos = Cultivo.objects.all().count()
    return num_cultivos

#función para contar las enfermedades registradas y retornarlas
def contarEnfermedades():
    num_enfermedades = Enfermedad.objects.all().count()
    return num_enfermedades

#función para contar los dataset registrados y retornarlos
def contarDatasets():
    num_datasets = Dataset.objects.all().count()
    return num_datasets

#función para contar los modelos registrados y retornarlos
def contarModelos():
    num_modelosYolov7 = Modelo_YOLOv7.objects.all().count()
    num_modelosTransformer = Modelo_Transformer.objects.all().count()
    num_modelos = num_modelosYolov7 + num_modelosTransformer
    return num_modelos

#función para contar los reportes registrados y retornarlos
# def contarReportes():
#     num_reportes = Reporte.objects.all().count()
#     return num_reportes


#función para redireccionar a la página principal del administrador
def inicioA(request):
    context = perfil(request)
    context['direccion'] =  'Administrador'
    context['num_usuarios'] = contarUsuarios()
    context['num_cultivos'] = contarCultivos()
    context['num_enfermedades'] = contarEnfermedades()
    context['num_datasets'] = contarDatasets()
    context['num_modelos'] = contarModelos()
    # context['num_reportes'] = contarReportes()

    return render(request, 'usuarios/administrador/inicioA.html', context)

#función para redireccionar a la página principal del experto
def inicioE(request):
    #obtener el id del usuario logueado
    id = request.user.id
    #obtener el usuario logueado
    usuario = User.objects.get(id=id)
    #obtener el experto logueado
    experto = Experto.objects.get(user_id=usuario.id)
    #obtener el nombre del experto logueado
    nombre = experto.nombre
    #obtener el apellido del experto logueado
    apellidoP = experto.apellidoP
    #obtener el correo del experto logueado
    correo = experto.correo
    #obtener la foto del experto logueado
    imagen = '/imagenes/'+str(experto.imagen)
    print("Imagen ", imagen)

    context = {'nombre': nombre, 'apellido': apellidoP, 'correo': correo, 'imagen': imagen}

    return render(request, 'usuarios/experto/inicioE.html', context)

#función para redireccionar a la página principal del tester
def inicioT(request):
    #obtener el id del usuario logueado
    id = request.user.id
    #obtener el usuario logueado
    usuario = User.objects.get(id=id)
    #obtener el tester logueado
    tester = Tester.objects.get(user_id=usuario.id)
    #obtener el nombre del tester logueado
    nombre = tester.nombre
    #obtener el apellido del tester logueado
    apellidoP = tester.apellidoP
    #obtener el correo del tester logueado
    correo = tester.correo
    #obtener la foto del tester logueado
    imagen = '/imagenes/'+str(tester.imagen)
    print("Imagen ", imagen)

    context = {'nombre': nombre, 'apellido': apellidoP, 'correo': correo, 'imagen': imagen}

    return render(request, 'usuarios/tester/inicioT.html', context)


#*****************************************************************************************************#
#**********                       GESTIÓN DE USUARIOS ADMINISTRADORES                       **********#
#*****************************************************************************************************#

def administradores(request): #función para redireccionar a la página donde se enlista todos los administradores 
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']   
    administradores = Administrador.objects.all().order_by('-id_Administrador')
    context = perfil(request)
    context['direccion'] =  'Administrador / Usuarios / Administradores'
    context['administradores'] = administradores
    context['regresar'] = 'http://{}/{}'.format(URL, 'Panel_administrador')

    return render(request, 'usuarios/administrador/indexA.html', context)

def crearAdministrador(request): #función para crear un nuevo administrador
    
    if request.method == 'POST':
        formularioUsuario = UsuarioForm(request.POST or None)
        formularioAdministrador = AdministradorForm(request.POST or None, request.FILES or None)
        # Se valida que los formularios sean válidos
        if formularioUsuario.is_valid() and formularioAdministrador.is_valid():
            # Se crean variables para los datos necesarios para realizar las operaciones siguientes
            id_administrador = formularioAdministrador.cleaned_data['id_Administrador']
            nombre = formularioAdministrador.cleaned_data['nombre']
            usuario = formularioUsuario.cleaned_data['username']

            # Se guardan los formularios de usuario y administrador
            formularioUsuario.save()
            formularioAdministrador.save()

            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
            
            # Se crea una sentencia para obtener el id del último usuario registrado
            last_id = conection.cursor()
            last_id.execute("""SELECT id FROM auth_user ORDER BY id DESC LIMIT 1""")
            id_usuario = last_id.fetchone()
            id_usuario = int(id_usuario[0])
            last_id.close()

            # Se crea una sentencia para actualizar el id del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE appsafecrops_administrador set user_id = %s WHERE id_Administrador = %s""", (id_usuario, id_administrador)) #se actualiza la ruta del dataset
            conection.commit()
            myquery.close()

            # Se envia un mensaje de registro exitoso al template
            messages.success(request, f'Administrador(a) {nombre} con usuario {usuario} creado correctamente')
            
            # Se redirecciona a la página de la lista de administradores
            return redirect('administradores')
        
        else:
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

            context = perfil(request)
            context['direccion'] =  'Administrador / Usuarios / Administradores / Registrar'
            context['formularioUsuario'] = formularioUsuario
            context['formularioAdministrador'] = formularioAdministrador
            context['regresar'] = 'http://{}/{}'.format(URL, 'administradores')
    else: # Si no se ha enviado el formulario
        URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
        formularioUsuario = UsuarioForm()
        formularioAdministrador = AdministradorForm()

        context = perfil(request)
        context['direccion'] =  'Administrador / Usuarios / Administradores / Registrar'
        context['formularioUsuario'] = formularioUsuario
        context['formularioAdministrador'] = formularioAdministrador
        context['regresar'] = 'http://{}/{}'.format(URL, 'administradores') 

    return render(request, 'usuarios/administrador/crear.html', context)

def editarAdministrador(request, id_Administrador, user_id): #función para editar un administrador con parametros de matricula
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
    
    # Se obtienen los datos personales del administrador
    administrador = Administrador.objects.get(id_Administrador=id_Administrador)
    formularioAdministrador = AdministradorForm(request.POST or None, request.FILES or None, instance=administrador)
    
    # Se obtienen los datos de usuario del administrador
    usuario = User.objects.get(id=user_id)
    formularioUsuario = UsuarioForm(request.POST or None, instance=usuario)

    # Se cambian los campos de contraseña a no requeridos
    formularioUsuario.fields['password1'].required = False
    formularioUsuario.fields['password2'].required = False

    if request.method == 'POST': # Si se ha enviado el formulario
        if not formularioUsuario.has_changed(): # Si no se ha modificado el usuario
            validation = True # Se valida el formulario con true
            username = usuario.username # Se obtiene el username del usuario
        else: # Si se ha modificado el usuario
            validation = formularioUsuario.is_valid() # Se valida el formulario de que el username no exista
            username = formularioUsuario.cleaned_data['username'] # Se obtiene el username del formulario
    
        if formularioAdministrador.is_valid() and validation == True: # Si los formularios son válidos
            nombre = formularioAdministrador.cleaned_data['nombre'] # Se obtiene el nombre del administrador del formulario
            
            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos

            # Se crea una sentencia para actualizar el username del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE auth_user set username = %s WHERE id = %s""", (username,user_id))
            conection.commit()
            myquery.close()
            
            formularioAdministrador.save()

            messages.success(request, f'Se ha modificado la información de administrador(a) {nombre} con usuario {username} correctamente')
            return redirect('administradores')
    else: # Si no se ha enviado el formulario  
        context = perfil(request)
        context['direccion'] =  'Administrador / Usuarios / Administradores / Modificar'
        context['formularioAdministrador'] = formularioAdministrador
        context['formularioUsuario'] = formularioUsuario
        context['administrador'] = administrador
        context['usuario'] = usuario
        context['regresar'] = 'http://{}/{}'.format(URL, 'administradores') 
         
    return render(request, 'usuarios/administrador/editar.html', context)

def eliminarAdministrador(request, id_Administrador): #función para eliminar un administrador con parametros de matricula
    administrador = Administrador.objects.get(id_Administrador=id_Administrador)
    usuario = User.objects.get(id=administrador.user_id)
    administrador.delete()
    usuario.delete()
    return redirect('administradores')


#*****************************************************************************************************#
#**********                           GESTIÓN DE USUARIOS EXPERTOS                          **********#
#*****************************************************************************************************#

def expertos(request): #función para redireccionar a la página donde se enlista todos los expertos
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    expertos = Experto.objects.all().order_by('-id_Experto')

    context = perfil(request)
    context['direccion'] =  'Administrador / Usuarios / Expertos'
    context['expertos'] = expertos
    context['regresar'] = 'http://{}/{}'.format(URL, 'Panel_administrador')

    return render(request, 'usuarios/experto/indexE.html', context)

def crearExperto(request): #función para crear un nuevo éxperto
    
    if request.method == 'POST':
        formularioUsuario = UsuarioForm(request.POST or None)
        formularioExperto = ExpertoForm(request.POST or None, request.FILES or None)
        # Se valida que los formularios sean válidos
        if formularioUsuario.is_valid() and formularioExperto.is_valid():
            # Se crean variables para los datos necesarios para realizar las operaciones siguientes
            nombre = formularioExperto.cleaned_data['nombre']
            usuario = formularioUsuario.cleaned_data['username']

            # Se guardan los formularios de usuario y administrador
            formularioUsuario.save()
            formularioExperto.save()

            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
            
            # Se crea una sentencia para obtener el id del último usuario registrado
            last_id = conection.cursor()
            last_id.execute("""SELECT id FROM auth_user ORDER BY id DESC LIMIT 1""")
            id_usuario = last_id.fetchone()
            id_usuario = int(id_usuario[0])
            last_id.close()

            last_id_experto = conection.cursor()
            last_id_experto.execute("""SELECT id_Experto FROM appsafecrops_experto ORDER BY id_Experto DESC LIMIT 1""")
            id_experto = last_id_experto.fetchone()
            id_experto = int(id_experto[0])
            last_id_experto.close()

            # Se crea una sentencia para actualizar el id del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE appsafecrops_experto set user_id = %s WHERE id_Experto = %s""", (id_usuario, id_experto)) #se actualiza la ruta del dataset
            conection.commit()
            myquery.close()

            # Se envia un mensaje de registro exitoso al template
            messages.success(request, f'Experto(a) {nombre} con usuario {usuario} creado correctamente')
            
            # Se redirecciona a la página de la lista de administradores
            return redirect('expertos')
        
        else:
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

            context = perfil(request)
            context['direccion'] =  'Administrador / Usuarios / Expertos / Regsitrar'
            context['formularioUsuario'] = formularioUsuario
            context['formularioExperto'] = formularioExperto
            context['regresar'] = 'http://{}/{}'.format(URL, 'expertos')
    else: # Si no se ha enviado el formulario
        URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
        formularioUsuario = UsuarioForm()
        formularioExperto = ExpertoForm()

        context = perfil(request)
        context['direccion'] =  'Administrador / Usuarios / Expertos / Regsitrar'
        context['formularioUsuario'] = formularioUsuario
        context['formularioExperto'] = formularioExperto
        context['regresar'] = 'http://{}/{}'.format(URL, 'expertos') 

    return render(request, 'usuarios/experto/crear.html', context)

def editarExperto(request, id_Experto, user_id): #función para editar un administrador con parametros de matricula
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
    
    # Se obtienen los datos personales del administrador
    experto = Experto.objects.get(id_Experto=id_Experto)
    formularioExperto = ExpertoForm(request.POST or None, request.FILES or None, instance=experto)
    
    # Se obtienen los datos de usuario del administrador
    usuario = User.objects.get(id=user_id)
    formularioUsuario = UsuarioForm(request.POST or None, instance=usuario)

    # Se cambian los campos de contraseña a no requeridos
    formularioUsuario.fields['password1'].required = False
    formularioUsuario.fields['password2'].required = False

    if request.method == 'POST': # Si se ha enviado el formulario
        if not formularioUsuario.has_changed(): # Si no se ha modificado el usuario
            validation = True # Se valida el formulario con true
            username = usuario.username # Se obtiene el username del usuario
        else: # Si se ha modificado el usuario
            validation = formularioUsuario.is_valid() # Se valida el formulario de que el username no exista
            username = formularioUsuario.cleaned_data['username'] # Se obtiene el username del formulario
    
        if formularioExperto.is_valid() and validation == True: # Si los formularios son válidos
            nombre = formularioExperto.cleaned_data['nombre'] # Se obtiene el nombre del administrador del formulario
            
            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos

            # Se crea una sentencia para actualizar el username del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE auth_user set username = %s WHERE id = %s""", (username,user_id))
            conection.commit()
            myquery.close()
            
            formularioExperto.save()

            messages.success(request, f'Se ha modificado la información de experto(a) {nombre} con usuario {username} correctamente')
            return redirect('expertos')
    
    else: # Si no se ha enviado el formulario
        context = perfil(request)
        context['direccion'] =  'Administrador / Usuarios / Expertos / Modificar'
        context['formularioExperto'] = formularioExperto
        context['formularioUsuario'] = formularioUsuario
        context['experto'] = experto
        context['usuario'] = usuario
        context['regresar'] = 'http://{}/{}'.format(URL, 'expertos') 
         
    return render(request, 'usuarios/experto/editar.html', context)

def eliminarExperto(request, id_Experto):
    experto = Experto.objects.get(id_Experto=id_Experto)
    usuario = User.objects.get(id=experto.user_id)
    experto.delete()
    usuario.delete()
    return redirect('expertos')


#*****************************************************************************************************#
#**********                           GESTIÓN DE USUARIOS TESTERS                           **********#
#*****************************************************************************************************#

def testers(request): #función para redireccionar a la página donde se enlista todos los testers
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    testers = Tester.objects.all().order_by('-id_Tester')

    context = perfil(request)
    context['direccion'] =  'Administrador / Usuarios / Testers'
    context['testers'] = testers
    context['regresar'] = 'http://{}/{}'.format(URL, 'Panel_administrador')

    return render(request, 'usuarios/tester/indexT.html', context)

def crearTester(request): #función para crear un nuevo éxperto
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    if request.method == 'POST':
        formularioUsuario = UsuarioForm(request.POST or None)
        formularioTester = TesterForm(request.POST or None, request.FILES or None)
        # Se valida que los formularios sean válidos
        if formularioUsuario.is_valid() and formularioTester.is_valid():
            # Se crean variables para los datos necesarios para realizar las operaciones siguientes
            nombre = formularioTester.cleaned_data['nombre']
            usuario = formularioUsuario.cleaned_data['username']

            # Se guardan los formularios de usuario y administrador
            formularioUsuario.save()
            formularioTester.save()

            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
            
            # Se crea una sentencia para obtener el id del último usuario registrado
            last_id = conection.cursor()
            last_id.execute("""SELECT id FROM auth_user ORDER BY id DESC LIMIT 1""")
            id_usuario = last_id.fetchone()
            id_usuario = int(id_usuario[0])
            last_id.close()

            last_id_tester = conection.cursor()
            last_id_tester.execute("""SELECT id_Tester FROM appsafecrops_tester ORDER BY id_Tester DESC LIMIT 1""")
            id_tester = last_id_tester.fetchone()
            id_tester = int(id_tester[0])
            last_id_tester.close()

            # Se crea una sentencia para actualizar el id del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE appsafecrops_tester set user_id = %s WHERE id_Tester = %s""", (id_usuario, id_tester)) #se actualiza la ruta del dataset
            conection.commit()
            myquery.close()

            # Se envia un mensaje de registro exitoso al template
            messages.success(request, f'Tester {nombre} con usuario {usuario} creado correctamente')
            
            # Se redirecciona a la página de la lista de administradores
            return redirect('testers')
    else: # Si no se ha enviado el formulario
        formularioUsuario = UsuarioForm()
        formularioTester = TesterForm()

        context = perfil(request)
        context['direccion'] =  'Administrador / Usuarios / Testers / Registrar'
        context['formularioUsuario'] = formularioUsuario
        context['formularioTester'] = formularioTester
        context['regresar'] = 'http://{}/{}'.format(URL, 'testers') 

    return render(request, 'usuarios/tester/crear.html', context)

def editarTester(request, id_Tester, user_id): #función para editar un administrador con parametros de matricula
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
    
    # Se obtienen los datos personales del administrador
    tester = Tester.objects.get(id_Tester=id_Tester)
    formularioTester = TesterForm(request.POST or None, request.FILES or None, instance=tester)
    
    # Se obtienen los datos de usuario del administrador
    usuario = User.objects.get(id=user_id)
    formularioUsuario = UsuarioForm(request.POST or None, instance=usuario)

    # Se cambian los campos de contraseña a no requeridos
    formularioUsuario.fields['password1'].required = False
    formularioUsuario.fields['password2'].required = False

    if request.method == 'POST': # Si se ha enviado el formulario
        if not formularioUsuario.has_changed(): # Si no se ha modificado el usuario
            validation = True # Se valida el formulario con true
            username = usuario.username # Se obtiene el username del usuario
        else: # Si se ha modificado el usuario
            validation = formularioUsuario.is_valid() # Se valida el formulario de que el username no exista
            username = formularioUsuario.cleaned_data['username'] # Se obtiene el username del formulario
    
        if formularioTester.is_valid() and validation == True: # Si los formularios son válidos
            nombre = formularioTester.cleaned_data['nombre'] # Se obtiene el nombre del administrador del formulario
            
            # Se crea una conexión a la base de datos
            conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos

            # Se crea una sentencia para actualizar el username del usuario en la tabla de administradores
            myquery=conection.cursor()
            myquery.execute("""UPDATE auth_user set username = %s WHERE id = %s""", (username,user_id))
            conection.commit()
            myquery.close()
            
            formularioTester.save()

            messages.success(request, f'Se ha modificado la información de tester {nombre} con usuario {username} correctamente')
            return redirect('testers')
    else: # Si no se ha enviado el formulario
        context = perfil(request)
        context['direccion'] =  'Administrador / Usuarios / Testers / Modificar'
        context['formularioTester'] = formularioTester
        context['formularioUsuario'] = formularioUsuario
        context['tester'] = tester
        context['usuario'] = usuario
        context['regresar'] = 'http://{}/{}'.format(URL, 'testers') 
         
    return render(request, 'usuarios/tester/editar.html', context)

def eliminarTester(request, id_Tester): #función para eliminar un tester con parametros de matricula
    tester = Tester.objects.get(id_Tester=id_Tester) #se obtiene el tester con la matricula
    usuario = User.objects.get(id=tester.user_id) #se obtiene el usuario del tester
    tester.delete() #se elimina el tester
    usuario.delete() #se elimina el usuario
    return redirect('testers') #se redirecciona a la página de testers


#*****************************************************************************************************#
#**********                          GESTIÓN DE PERFIL DE USUARIOS                          **********#
#*****************************************************************************************************#

def usuarios(request): #función para redireccionar a la página donde se enlista todos los usuarios
    usuarios = User.objects.all().order_by('-id')

    context = perfil(request)
    context['direccion'] =  'Administrador / Usuarios'
    context['usuarios'] = usuarios
    
    return render(request, 'usuarios/usuario/indexU.html', context)

def eliminarUsuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('usuarios')


#*****************************************************************************************************#
#**********                             GESTIÓN DE ENFERMEDADES                             **********#
#*****************************************************************************************************#

def enfermedades(request): #función para redireccionar a la página donde se enlista todas las enfermedades
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    enfermedades = Enfermedad.objects.all().order_by('-id_Enfermedad')

    context = perfil(request)
    context['direccion'] =  'Administrador / Enfermedades'
    context['enfermedades'] = enfermedades
    context['regresar'] = 'http://{}/{}'.format(URL, 'Panel_administrador')

    return render(request, 'enfermedades/indexE.html', context)

def crearEnfermedad(request):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    formulario = EnfermedadForm(request.POST or None)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombreEnfermedad']
        messages.success(request, f'Enfermedad {nombre} creada correctamente')
        formulario.save()
        return redirect('enfermedades')
    
    context = perfil(request)
    context['direccion'] =  'Administrador / Enfermedades / Registrar'
    context['formulario'] = formulario
    context['regresar'] = 'http://{}/{}'.format(URL, 'enfermedades') 

    return render(request, 'enfermedades/crear.html', context)

def editarEnfermedad(request, id_Enfermedad):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    enfermedad = Enfermedad.objects.get(id_Enfermedad=id_Enfermedad)
    cultivo = Cultivo.objects.all()
    formulario = EnfermedadForm(request.POST or None, instance=enfermedad)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombreEnfermedad']
        messages.success(request, f'Enfermedad {nombre} modificada correctamente')
        formulario.save()
        return redirect('enfermedades')
    
    context = perfil(request)
    context['direccion'] =  'Administrador / Enfermedades / Modificar'
    context['formulario'] = formulario
    context['enfermedad'] = enfermedad
    context['cultivos'] = cultivo
    context['regresar'] = 'http://{}/{}'.format(URL, 'enfermedades') 

    return render(request, 'enfermedades/editar.html', context)

def eliminarEnfermedad(request, id_Enfermedad):
    enfermedad = Enfermedad.objects.get(id_Enfermedad=id_Enfermedad)
    enfermedad.delete()
    return redirect('enfermedades')


#*****************************************************************************************************#
#**********                               GESTIÓN DE DATASETS                               **********#
#*****************************************************************************************************#

def datasets(request): #función para redireccionar a la página donde se enlista todos los datasets
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    datasets = Dataset.objects.all().order_by('-id_Dataset')

    estadoDataset = request.GET.get('estadoDataset')
    if estadoDataset == 'Todos' or estadoDataset == None:
        datasets = Dataset.objects.all()
    elif estadoDataset == 'Activo':
        datasets = Dataset.objects.filter(estadoDataset='Activo')
    elif estadoDataset == 'Inactivo':
        datasets = Dataset.objects.filter(estadoDataset='Inactivo')

    context = perfil(request)
    context['direccion'] =  'Administrador / Datasets'
    context['datasets'] = datasets
    context['regresar'] = 'http://{}/{}'.format(URL, 'Panel_administrador')

    return render(request, 'datasets/indexD.html', context)

def crearDataset(request):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    if request.method == 'POST':
        formulario = DatasetForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            rutaName = formulario.cleaned_data['ruta'].name
            nombreD = formulario.cleaned_data['nombreDataset']
            formatoImagen = formulario.cleaned_data['formatoImg']
            rutaOrigen = settings.MEDIA_ROOT + 'datasets/' + rutaName
            rutaDestino = settings.MEDIA_ROOT + 'datasets/' + nombreD
            try:
                print("Fuera 1 ")
                respuesta_sentencia = Zip.descomprimir(rutaOrigen, rutaDestino, formatoImagen, nombreD)
                print("Fuera 2 ")
            except NameError:
                messages.error(request, f'Hubo un problema al crear el dataset {nombreD} en la parte de extracción del archivo .zip')
                os.remove(rutaOrigen)
                shutil.rmtree(rutaDestino)

                # Consultar el último ID registrado en la tabla datasets 
                conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
                last_id = conection.cursor()
                last_id.execute("""SELECT id_Dataset FROM appsafecrops_dataset ORDER BY id_Dataset DESC LIMIT 1""") #se obtiene el id del ultimo dataset
                id_dataset = last_id.fetchone()
                last_id.close()

                # Eliminar el regitro de la base de datos
                myquery=conection.cursor()
                myquery.execute("""DELETE FROM appsafecrops_dataset WHERE id_Dataset = %s""", (id_dataset)) #se actualiza la ruta del dataset
                conection.commit() #se confirma la eliminación
                myquery.close() #se cierra el cursor

                return redirect('crearDataset')
            print(respuesta_sentencia)
            if respuesta_sentencia != 'ok':
                if respuesta_sentencia == 'error_nombre_carpetas':
                    messages.error(request, f'El archivo {rutaName} no cuenta con los nombres de carpeta train y/o validation')
                    shutil.rmtree(rutaDestino)
                elif respuesta_sentencia == 'error_no_clases':
                    messages.error(request, f'El dataset no contiene ninguna clase de enfermedad')
                    shutil.rmtree(rutaDestino)
                elif respuesta_sentencia == 'error_numero_clases':
                    messages.error(request, f'El dataset debe contener por lo menos 2 clases de enfermedades')
                    shutil.rmtree(rutaDestino)

                # Consultar el último ID registrado en la tabla datasets 
                conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos
                last_id = conection.cursor()
                last_id.execute("""SELECT id_Dataset FROM appsafecrops_dataset ORDER BY id_Dataset DESC LIMIT 1""") #se obtiene el id del ultimo dataset
                id_dataset = last_id.fetchone()
                last_id.close()

                # Eliminar el regitro de la base de datos
                myquery=conection.cursor()
                myquery.execute("""DELETE FROM appsafecrops_dataset WHERE id_Dataset = %s""", (id_dataset)) #se actualiza la ruta del dataset
                conection.commit() #se confirma la eliminación
                myquery.close() #se cierra el cursor

                return redirect('crearDataset')
            else:
                messages.success(request, f'Dataset {nombreD} creado correctamente')
                return redirect('datasets')
            
        else:
            messages.error(request, 'Error al crear el dataset.')
            #formulario = DatasetForm()

            context = perfil(request)
            context['direccion'] =  'Administrador / Datasets / Registrar'
            context['formulario'] = formulario
            context['regresar'] = 'http://{}/{}'.format(URL, 'datasets')
    else:
        formulario = DatasetForm()

        context = perfil(request)
        context['direccion'] =  'Administrador / Datasets / Registrar'
        context['formulario'] = formulario
        context['regresar'] = 'http://{}/{}'.format(URL, 'datasets')

    return render(request, 'datasets/crear.html', context)

def verDataset(request, id_Dataset):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    nombre = dataset.nombreDataset
    rutaDataset = dataset.ruta.name

    rutaDatasetTrain = '/datasets/'+dataset.ruta.name+'/train/'

    # Lista de extensiones de archivo de imagen que deseas considerar
    extensiones_imagen = ['.jpg', '.jpeg', '.png', '.webp']

    diccionarioTrain = {}
    diccionarioValidation = {}

    for division_file in os.listdir(rutaDataset):
        for enfermedad in os.listdir(os.path.join(rutaDataset, division_file)):
            imagenes = []

            for imagen in os.listdir(os.path.join(rutaDataset, division_file, enfermedad)):
                if any(imagen.endswith(ext) for ext in extensiones_imagen):
                    imagenes.append(imagen)

            if division_file == 'train':
                if 'train' not in diccionarioTrain:
                    diccionarioTrain['train'] = []
                diccionarioTrain['train'].append({'enfermedad':enfermedad, 'imagenes':imagenes})
            elif division_file == 'validation':
                if 'validation' not in diccionarioValidation:
                    diccionarioValidation['validation'] = []
                diccionarioValidation['validation'].append({'enfermedad':enfermedad, 'imagenes':imagenes})

    rutaDatasetValidation = '/datasets/'+dataset.ruta.name+'/validation/'

    context = perfil(request)
    context['direccion'] =  'Administrador / Datasets / '+nombre
    context['diccionarioTrain'] = diccionarioTrain
    context['diccionarioValidation'] = diccionarioValidation
    context['id_Dataset'] = id_Dataset
    context['datasetTrain'] = rutaDatasetTrain
    context['datasetValidation'] = rutaDatasetValidation
    context['dataset_info'] = dataset
    context['numImagenes'] = dataset.numImgTotal
    context['numTrain'] = dataset.numImgEntrenamiento
    context['numValidation'] = dataset.numImgValidacion
    context['regresar'] = 'http://{}/{}'.format(URL, 'datasets') 

    return render(request, 'datasets/ver.html', context)

def editarDataset(request, id_Dataset):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    formulario = DatasetForm(request.POST or None, request.FILES or None, instance=dataset)

    # Se recuperan los datos antes de modificar el dataset
    rutaAnterior = dataset.ruta.name
    numImgTotal = dataset.numImgTotal
    numImgEntrenamiento = dataset.numImgEntrenamiento
    numImgValidacion = dataset.numImgValidacion

    # Se valida que el formulario sea válido
    if formulario.is_valid():
        # Se guardan los datos del formulario
        formulario.save()
        
        # Se obtienen los datos del formulario
        tipo = formulario.cleaned_data['tipoDataset']
        nombreD = formulario.cleaned_data['nombreDataset']
        formatoImagen = formulario.cleaned_data['formatoImg']
        rutaName = formulario.cleaned_data['ruta'].name
        ruta_split = rutaName.split('.')
        if len(ruta_split) > 1:
            shutil.rmtree(rutaAnterior) #se elimina la carpeta del dataset anterior
            Zip.descomprimir(str(formulario.instance.ruta.name), rutaName, tipo, nombreD, formatoImagen) #se descomprime el nuevo dataset
        else:
            dataset.ruta = rutaAnterior
            dataset.numImgTotal = numImgTotal
            dataset.numImgEntrenamiento = numImgEntrenamiento
            dataset.numImgValidacion = numImgValidacion
            dataset.save()
        messages.success(request, f'Dataset {nombreD} modificado correctamente')
        return redirect('datasets')
    
    context = perfil(request)
    context['direccion'] =  'Administrador / Datasets / Modificar'
    context['formulario'] = formulario
    context['dataset'] = dataset
    context['regresar'] = 'http://{}/{}'.format(URL, 'datasets') 

    return render(request, 'datasets/editar.html', context)

def eliminarDataset(request, id_Dataset):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    dataset.delete()
    return redirect('datasets')

def activarDataset(request, id_Dataset):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    dataset.estadoDataset = 'Activo'
    dataset.save()
    messages.success(request, f'Dataset {dataset.nombreDataset} activado correctamente')
    return redirect('datasets')

def desactivarDataset(request, id_Dataset):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    dataset.estadoDataset = 'Inactivo'
    dataset.save()
    return redirect('datasets')

def eliminarImagen(request, id_Dataset, imagen):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    nombre = dataset.nombreDataset
    ruta = dataset.ruta.name
    if os.path.exists(ruta+'/train/'+imagen):
        os.remove(ruta+'/train/'+imagen)

        num_imagenes = contarImagenes(request, id_Dataset)

        # Se crea una conexión a la base de datos
        conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos

        # Se crea una sentencia para actualizar el número de imagenes en la tabla de datasets
        myquery=conection.cursor()
        myquery.execute("""UPDATE appsafecrops_dataset set numImgTotal = %s, numImgEntrenamiento = %s WHERE id_Dataset = %s""", (num_imagenes[0], num_imagenes[1], id_Dataset)) #se actualiza la ruta del dataset
        conection.commit()
        myquery.close()

    elif os.path.exists(ruta+'/validacion/'+imagen):
        os.remove(ruta+'/validacion/'+imagen)

        num_imagenes = contarImagenes(request, id_Dataset)

        # Se crea una conexión a la base de datos
        conection= mysql.connector.connect(user='root', database='id21050120_safecrops', host='localhost', port='3306', password='') #se conecta a la base de datos

        # Se crea una sentencia para actualizar el número de imagenes en la tabla de datasets
        myquery=conection.cursor()
        myquery.execute("""UPDATE appsafecrops_dataset set numImgTotal = %s, numImgValidacion = %s WHERE id_Dataset = %s""", (num_imagenes[0], num_imagenes[2], id_Dataset)) #se actualiza la ruta del dataset
        conection.commit()
        myquery.close()

    return redirect('verDataset', id_Dataset)

def contarImagenes(request, id_Dataset):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    ruta = dataset.ruta.name
    dirsTrain = os.listdir(ruta+'/train')
    dirsValidation = os.listdir(ruta+'/validation')
    n_img_total = len(dirsTrain) + len(dirsValidation)
    num_imagenes = [n_img_total, len(dirsTrain), len(dirsValidation)]
    return num_imagenes

#*****************************************************************************************************#
#**********                               GESTIÓN DE CULTIVOS                               **********#
#*****************************************************************************************************#

def cultivos(request): #función para redireccionar a la página donde se enlista todos los cultivos
    cultivos = Cultivo.objects.all().order_by('-id_Cultivo')

    context = perfil(request)
    context['direccion'] =  'Administrador / Cultivos'
    context['cultivos'] = cultivos

    return render(request, 'cultivos/indexC.html', context)

def crearCultivo(request):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    formulario = CultivoForm(request.POST or None)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombreCultivo']
        messages.success(request, f'Cultivo {nombre} creado correctamente')
        formulario.save()
        return redirect('cultivos')
    
    context = perfil(request)
    context['direccion'] =  'Administrador / Cultivos / Registrar'
    context['formulario'] = formulario
    context['regresar'] = 'http://{}/{}'.format(URL, 'cultivos') 

    return render(request, 'cultivos/crear.html', context)

def editarCultivo(request, id_Cultivo):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    cultivo = Cultivo.objects.get(id_Cultivo=id_Cultivo)
    formulario = CultivoForm(request.POST or None, instance=cultivo)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombreCultivo']
        messages.success(request, f'Cultivo {nombre} modificado correctamente')
        formulario.save()
        return redirect('cultivos')
    
    context = perfil(request)
    context['direccion'] =  'Administrador / Cultivos / Modificar'
    context['formulario'] = formulario
    context['cultivo'] = cultivo
    context['regresar'] = 'http://{}/{}'.format(URL, 'cultivos') 

    return render(request, 'cultivos/editar.html', context)

def eliminarCultivo(request, id_Cultivo):
    cultivo = Cultivo.objects.get(id_Cultivo=id_Cultivo)
    cultivo.delete()
    return redirect('cultivos')


#*****************************************************************************************************#
#**********                               GESTIÓN DE MODELOS                                **********#
#*****************************************************************************************************#

def modelos(request): #función para redireccionar a la página donde se enlista todos los modelos
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    modelosYOLOv7 = Modelo_YOLOv7.objects.all()
    modelosTransformer = Modelo_Transformer.objects.all()

    context = perfil(request)
    context['direccion'] =  'Administrador / Modelos'
    context['modelosYOLOv7'] = modelosYOLOv7
    context['modelosTransformer'] = modelosTransformer
    context['regresar'] = 'http://{}/{}'.format(URL, 'Panel_administrador')

    return render(request, 'modelos/indexM.html', context)

def seleccionarArquitectura(request):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    if request.method == 'POST':
        # formularioYOLOv3 = Modelo_YOLOv3_Form(request.POST, request.FILES)
        # formularioYOLOv5 = Modelo_YOLOv5_Form(request.POST, request.FILES)
        formularioYOLOv7 = Modelo_YOLOv7_Form(request.POST, request.FILES)
        formularioTransformer = Modelo_Transformer_Form(request.POST, request.FILES)

        

        if formularioYOLOv7.is_valid() or formularioTransformer.is_valid():
            # if formularioYOLOv3.is_valid():
            #     formularioYOLOv3.save()
            #     messages.success(request, f'Modelo YOLOv3 creado correctamente')
            #     return redirect('modelos')
            # if formularioYOLOv5.is_valid():
            #     formularioYOLOv5.save()
            #     messages.success(request, f'Modelo YOLOv5 creado correctamente')
            #     return redirect('modelos')

            if formularioYOLOv7.is_valid():
                # Valores obtenidos del formulario 
                nombreYOLOv7 = formularioYOLOv7.cleaned_data['nombreModelo_y7']
                nombreDataset = formularioYOLOv7.cleaned_data['datasetModelo_y7']
                epocas = formularioYOLOv7.cleaned_data['epocas_y7']
                batch_size = formularioYOLOv7.cleaned_data['batch_size_y7']

                query_dataset = query_ruta_dataset(str(nombreDataset))

                # Variables para documento .yaml
                dir_train = os.path.join(str(query_dataset[0]), "train/")
                dir_val = os.path.join(str(query_dataset[0]), "validation/")
                n_clases = query_dataset[1]
                nombres_clases = str(query_dataset[2]).split('[')
                nombres_clases = str(nombres_clases[1]).split(']')
                nombres_clases = str(nombres_clases[0])
                print(os.getcwd())
                cd("AppSafeCrops/MODELO_YOLOv7")

                # Creación del archivo custom_data.yaml
                file = open(os.path.join(HOME, "AppSafeCrops","MODELO_YOLOv7","data","custom_data.yaml"), "w")
                print("Archivo creado")
                file.write(f"train: {dir_train}" + os.linesep)
                file.write(f"val: {dir_val}" + os.linesep)
                file.write(f"nc: {n_clases}" + os.linesep)
                file.write(f"names: [ {nombres_clases} ]" + os.linesep)
                file.close()

                # Modificar el archivo yolov7-tiny-custom
                with open (os.path.join(HOME,"AppSafeCrops","MODELO_YOLOv7","cfg","training","yolov7-tiny-custom.yaml"),"r") as archivo:
                    lineas = archivo.readlines()
                
                #Modificar la primer línea del archivo
                lineas[0] = f"nc: {n_clases}"
                print(lineas)

                #Escribir el contenido actualizado al archivo
                with open(os.path.join(HOME,"AppSafeCrops","MODELO_YOLOv7","cfg","training","yolov7-tiny-custom.yaml"),"w") as archivo:
                    archivo.writelines(lineas)
                    #archivo.seek(0)
                    #archivo.writelines(lineas)
                    #archivo.truncate()
                

                # Proceso para realizar el entrenamiento de YOLOv7 con parámetros
                subprocess.call([sys.executable, '-m', 'train','--device', '0', '--batch-size', str(batch_size), '--epochs', str(epocas), '--img', '640', '640', '--data', 'data/custom_data.yaml', '--cfg', 'cfg/training/yolov7-tiny-custom.yaml', '--name', nombreYOLOv7, '--weights', 'yolov7-tiny.pt'])
                formularioYOLOv7.save()
                cd(HOME)
                print(os.getcwd())
                messages.success(request, f'Modelo YOLOv7 creado correctamente')
                return redirect('modelos')
            if formularioTransformer.is_valid():
                nombreTransformer = formularioTransformer.cleaned_data['nombreModelo_transformer']
                nombreDataset = formularioTransformer.cleaned_data['datasetModelo_transformer']
                epocas = formularioTransformer.cleaned_data['epocas_transformer']
                batch_size = formularioTransformer.cleaned_data['batch_size_transformer']

                Transformer.training_model(nombreTransformer, nombreDataset, epocas, batch_size)
                formularioTransformer.save()
                messages.success(request, f'Modelo Transformer creado correctamente')
                return redirect('modelos')
        else:
            messages.error(request, 'Error al crear el modelo.')
            formularioYOLOv7 = Modelo_YOLOv7_Form()
            formularioTransformer = Modelo_Transformer_Form()

            context = perfil(request)
            context['direccion'] =  'Administrador / Modelos / Arquitectura'
            context['formularioYOLOv7'] = formularioYOLOv7
            context['formularioTransformer'] = formularioTransformer
            context['regresar'] = 'http://{}/{}'.format(URL, 'modelos')
    else:
        formularioYOLOv7 = Modelo_YOLOv7_Form()
        formularioTransformer = Modelo_Transformer_Form()

        context = perfil(request)
        context['direccion'] =  'Administrador / Modelos / Arquitectura'
        context['formularioYOLOv7'] = formularioYOLOv7
        context['formularioTransformer'] = formularioTransformer
        context['regresar'] = 'http://{}/{}'.format(URL, 'modelos')

    return render(request, 'modelos/seleccionarArquitectura.html', context)

def crearModelo_YOLOv7(request):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    if request.method == 'POST':
        formulario = Modelo_YOLOv7_Form(request.POST, request.FILES)

        if formulario.is_valid():
            
            formulario.save()
            messages.success(request, f'Modelo creado correctamente')
            return redirect('modelos')
        else:
            messages.error(request, 'Error al crear el modelo.')
            formulario = Modelo_YOLOv7_Form()

            context = perfil(request)
            context['direccion'] =  'Administrador / Modelos / Registrar'
            context['formulario'] = formulario
            context['regresar'] = 'http://{}/{}'.format(URL, 'seleccionarArquitectura')
    else:
        formulario = Modelo_YOLOv7_Form()

        context = perfil(request)
        context['direccion'] =  'Administrador / Modelos / Registrar'
        context['formulario'] = formulario
        context['regresar'] = 'http://{}/{}'.format(URL, 'modelos')

    return render(request, 'modelos/crear.html', context)

def editarModelo_YOLOv7(request, id_Modelo):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    modelo = Modelo_YOLOv7.objects.get(id_Modelo=id_Modelo)
    formulario = Modelo_YOLOv7_Form(request.POST or None, request.FILES or None, instance=modelo)
    if formulario.is_valid():
        messages.success(request, f'Modelo modificado correctamente')
        formulario.save()
        return redirect('modelos')
    
    context = perfil(request)
    context['direccion'] =  'Administrador / Modelos / Modificar'
    context['formulario'] = formulario
    context['modelo'] = modelo
    context['regresar'] = 'http://{}/{}'.format(URL, 'modelos') 

    return render(request, 'modelos/editar.html', context)

def eliminarModelo_YOLOv7(request, id_Modelo):
    modelo = Modelo_YOLOv7.objects.get(id_Modelo=id_Modelo)
    modelo.delete()
    return redirect('modelos')

def crearModeloTransformer(request):
    URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']

    if request.method == 'POST':
        formulario = Modelo_Transformer_Form(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'Modelo creado correctamente')
            return redirect('modelos')
        else:
            messages.error(request, 'Error al crear el modelo.')
            formulario = Modelo_Transformer_Form()

            context = perfil(request)
            context['direccion'] =  'Administrador / Modelos / Registrar'
            context['formulario'] = formulario
            context['regresar'] = 'http://{}/{}'.format(URL, 'seleccionarArquitectura')
    else:
        formulario = Modelo_Transformer_Form()

        context = perfil(request)
        context['direccion'] =  'Administrador / Modelos / Registrar'
        context['formulario'] = formulario
        context['regresar'] = 'http://{}/{}'.format(URL, 'modelos')

    return render(request, 'modelos/crear.html', context)
