
import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required 
from .models import Administrador, Experto, Tester, Enfermedad, Dataset
from .forms import AdministradorForm, ExpertoForm, TesterForm, UsuarioForm, ResetPasswordForm, ChangePasswordForm, EnfermedadForm, DatasetForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from .zip import Zip
#import mysql.connector

###################################
# Send Email

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
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives

# Create your views here.

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
        
    return render(request, 'registration/login.html', {'form': fm})
'''
def ResetPassword(request):
    form_class = ResetPasswordForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy(settings.LOGIN_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResetPassword, self).dispatch(*args, **kwargs)
    
    def send_email_reset_pwd(self, user):

        # subject = "Restablecer contraseña Safe Crops"
        # template = get_template('registration/send_email_reset_pwd.html')

        # content = template.render({'user': user})

        # message = EmailMultiAlternatives(subject, 'Mensaje importante', settings.EMAIL_HOST_USER, [user.email])

        # message.attach_alternative(content, 'text/html')
        # message.send()
        # print("Correo enviado correctamente")

        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("Conectado...")
        email_to = "campeon2311@gmail.com"

        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Tienes un correo de SafeCrops"

        content = render_to_string('send_email_reset_pwd.html', {
            'user': User.objects.get(pk=1)})
        mensaje.attach(MIMEText(content, 'html'))

        mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())

        print("Correo enviado correctamente")

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            data = self.send_email_reset_pwd(user)
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})


    return render(request, 'registration/password_reset.html', {'form': form_class})
'''
'''
def ResetPassword(request):
    form_class = ResetPasswordForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy(settings.REGISTRATION_REDIRECT_URL)

    def send_email_reset_pwd(self, user):
        data = {}
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña'

            content = render_to_string('registration/send_email_reset_pwd.html', {
                'user': user,
                'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
            print("Mensaje enviado")
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)  # self.get_form()
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_pwd(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        return context
    
    return render(request, 'registration/password_reset.html', {'form': form_class})
'''
# FUNCIONA ENVIO DE CORREO
'''
def sendEmail(mail,request):
    context={'mail':mail}
    template = get_template('registration/send_email_reset_pwd.html')
    content = template.render(context)
    
    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'CodigoFacilito',
        settings.EMAIL_HOST_USER,#Origen
        [mail],#Destinatarios

    )
    email.attach_alternative(content,'text/html')
    email.send()
'''
    
# FUNCIONA ENVIO DE CORREO
'''
def ResetPassword(request):
    form_class = ResetPasswordForm(request.POST or None)
    usuarios = User.objects.all()

    if request.method == 'POST':
        
        for user in usuarios:
            if user.email == 'dcao201793@upemor.edu.mx':
                print("Entro a query exists", user.email)
                sendEmail(user.email,request)
                messages.success(request, f'Correo enviado correctamente')

    return render(request, 'registration/password_reset.html', {'form': form_class})
'''

#FUNCIONA ENVIO DE CORREO

def sendEmail(request):
    mail = request.GET.get('email')
    queryEmail = User.objects.all()
    
    bandera = False
    
    for user in queryEmail:
        if mail == user.email:
            print("Enviar correo a", mail)
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()
            context={
                'mail':mail, 
                'user':user,
                'link_resetpwd': 'http://{}/change_password/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
                }
            template = get_template('registration/send_email_reset_pwd.html')
            content = render_to_string('registration/send_email_reset_pwd.html', context)
            
            email = EmailMultiAlternatives(
                'Un correo de prueba',
                'CodigoFacilito',
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

def ResetPassword(request):
    form_class = ResetPasswordForm(request.GET or None)
    return render(request, 'registration/password_reset.html', {'form': form_class})

'''
def changePassword(request, token):
    form_class = ChangePasswordForm(request.POST or None)
    usuarios = User.objects.all()
    
    for user in usuarios:
        if User.objects.filter(token=token).exists():
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST)
                if form.is_valid():
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    messages.success(request, f'Contraseña cambiada correctamente')
                    return redirect('login/')
            else:
                form = ChangePasswordForm()
            return render(request, 'registration/change_password.html', {'form': form_class})
    return redirect('login/')
'''
def ChangePass(request, token):
    form_class = ChangePasswordForm(request.POST or None)
    usuarios = User.objects.all()
    
    for user in usuarios:
        if User.objects.filter(token=token).exists():
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST)
                if form.is_valid():
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    messages.success(request, f'Contraseña cambiada correctamente')
                    return redirect('login/')
            else:
                form = ChangePasswordForm()
            return render(request, 'registration/change_password.html', {'form': form_class})
    return redirect('login/' )

def ChangePassword(request, token):
    form_class = ChangePasswordForm(request.POST or None)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return get(request, *args, **kwargs)
        return redirect('passwordReset')



def user_profile(request):
    return render(request, 'usuarios/tester/inicioT.html')

# función para cerrar sesión
def salir(request):
    logout(request)
    return redirect('login/')

#función para redireccionar a la página de inicio principal
def inicio(request):
    return render(request, 'paginas/inicio.html')

#función para redireccionar a la página principal del administrador
def inicioA(request):
    return render(request, 'usuarios/administrador/inicioA.html')

#función para redireccionar a la página principal del experto
def inicioE(request):
    return render(request, 'usuarios/experto/inicioE.html')

#función para redireccionar a la página principal del tester
def inicioT(request):
    return render(request, 'usuarios/tester/inicioT.html')


def administradores(request): #función para redireccionar a la página donde se enlista todos los administradores
    administradores = Administrador.objects.all()
    return render(request, 'usuarios/administrador/indexA.html', {'administradores': administradores})

def crearAdministrador(request): #función para crear un nuevo administrador
    formulario = AdministradorForm(request.POST or None, request.FILES or None) #se crea un formulario con los datos del administrador
    if formulario.is_valid(): #si el formulario es válido
        nombre = formulario.cleaned_data['nombre'] #se obtiene el nombre del administrador
        messages.success(request, f'Administrador(a) {nombre} creado correctamente') #se muestra un mensaje de éxito
        formulario.save() #se guarda el formulario
        return redirect('administradores') #se redirecciona a la página de administradores
    return render(request, 'usuarios/administrador/crear.html', {'formulario': formulario}) #se renderiza la página de crear administrador

def editarAdministrador(request, id_Administrador): #función para editar un administrador con parametros de matricula
    administrador = Administrador.objects.get(id_Administrador=id_Administrador)
    formulario = AdministradorForm(request.POST or None, request.FILES or None, instance=administrador)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombre']
        messages.success(request, f'Se ha modificado la información de administrador(a) {nombre} correctamente')
        formulario.save()
        return redirect('administradores')
    return render(request, 'usuarios/administrador/editar.html', {'formulario': formulario, 'administrador': administrador})

def eliminarAdministrador(request, id_Administrador): #función para eliminar un administrador con parametros de matricula
    administrador = Administrador.objects.get(id_Administrador=id_Administrador)
    administrador.delete()
    return redirect('administradores')


def expertos(request): #función para redireccionar a la página donde se enlista todos los expertos
    expertos = Experto.objects.all()
    return render(request, 'usuarios/experto/indexE.html', {'expertos': expertos})

def crearExperto(request):
    formulario = ExpertoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombre']
        messages.success(request, f'Experto(a) {nombre} creado correctamente')
        formulario.save()
        return redirect('expertos')
    return render(request, 'usuarios/experto/crear.html', {'formulario': formulario})

def editarExperto(request, id_Experto):
    experto = Experto.objects.get(id_Experto=id_Experto)
    formulario = ExpertoForm(request.POST or None, request.FILES or None, instance=experto)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombre']
        messages.success(request, f'Se ha modificado la información de experto(a) {nombre} correctamente')
        formulario.save()
        return redirect('expertos')
    return render(request, 'usuarios/experto/editar.html', {'formulario': formulario, 'experto': experto})

def eliminarExperto(request, id_Experto):
    experto = Experto.objects.get(id_Experto=id_Experto)
    experto.delete()
    return redirect('expertos')


def testers(request): #función para redireccionar a la página donde se enlista todos los testers
    testers = Tester.objects.all()
    return render(request, 'usuarios/tester/indexT.html', {'testers': testers})

def crearTester(request): #función para crear un nuevo tester
    formulario = TesterForm(request.POST or None, request.FILES or None) #se crea un formulario con los datos del tester
    if formulario.is_valid(): #si el formulario es válido
        nombre = formulario.cleaned_data['nombre']
        messages.success(request, f'Tester {nombre} creado correctamente')
        formulario.save() #se guarda el formulario
        return redirect('testers') #se redirecciona a la página de testers
    return render(request, 'usuarios/tester/crear.html', {'formulario': formulario}) #se renderiza la página de crear tester

def editarTester(request, id_Tester): #función para editar un tester con parametros de matricula
    tester = Tester.objects.get(id_Tester=id_Tester) #se obtiene el tester con la matricula
    formulario = TesterForm(request.POST or None, request.FILES or None, instance=tester) #se crea un formulario con los datos del Tester
    if formulario.is_valid(): #si el formulario es válido
        nombre = formulario.cleaned_data['nombre']
        messages.success(request, f'Se ha modificado la información de tester {nombre} correctamente')
        formulario.save() #se guarda el formulario
        return redirect('testers') #se redirecciona a la página de testers
    return render(request, 'usuarios/tester/editar.html', {'formulario': formulario, 'tester': tester}) #se renderiza la página de editar alumno

def eliminarTester(request, id_Tester): #función para eliminar un tester con parametros de matricula
    tester = Tester.objects.get(id_Tester=id_Tester) #se obtiene el tester con la matricula
    tester.delete() #se elimina el tester
    return redirect('testers') #se redirecciona a la página de testers


def usuarios(request): #función para redireccionar a la página donde se enlista todos los usuarios
    usuarios = User.objects.all()
    return render(request, 'usuarios/usuario/indexU.html', {'usuarios': usuarios})

def crearUsuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado correctamente')
            formulario.save()
            return redirect('usuarios')
    else:
        formulario = UsuarioForm()
    return render(request, 'usuarios/usuario/crear.html', {'formulario': formulario})

def editarUsuario(request, id):
    usuario = User.objects.get(id=id)
    formulario = UsuarioForm(request.POST or None, instance=usuario)
    if formulario.is_valid():
        username = formulario.cleaned_data['username']
        messages.success(request, f'Usuario {username} modificado correctamente')
        formulario.save()
        return redirect('usuarios')
    return render(request, 'usuarios/usuario/editar.html', {'formulario': formulario, 'usuario': usuario})

def eliminarUsuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('usuarios')


def enfermedades(request): #función para redireccionar a la página donde se enlista todas las enfermedades
    enfermedades = Enfermedad.objects.all()
    return render(request, 'enfermedades/indexE.html', {'enfermedades': enfermedades})

def crearEnfermedad(request):
    formulario = EnfermedadForm(request.POST or None)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombreEnfermedad']
        messages.success(request, f'Enfermedad {nombre} creada correctamente')
        formulario.save()
        return redirect('enfermedades')
    return render(request, 'enfermedades/crear.html', {'formulario': formulario})

def editarEnfermedad(request, id_Enfermedad):
    enfermedad = Enfermedad.objects.get(id_Enfermedad=id_Enfermedad)
    formulario = EnfermedadForm(request.POST or None, instance=enfermedad)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombreEnfermedad']
        messages.success(request, f'Enfermedad {nombre} modificada correctamente')
        formulario.save()
        return redirect('enfermedades')
    return render(request, 'enfermedades/editar.html', {'formulario': formulario, 'enfermedad': enfermedad})

def eliminarEnfermedad(request, id_Enfermedad):
    enfermedad = Enfermedad.objects.get(id_Enfermedad=id_Enfermedad)
    enfermedad.delete()
    return redirect('enfermedades')

def datasets(request): #función para redireccionar a la página donde se enlista todos los datasets
    datasets = Dataset.objects.all()
    return render(request, 'datasets/indexD.html', {'datasets': datasets})

def crearDataset(request):
    if request.method == 'POST':
        formulario = DatasetForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            rutaName = formulario.cleaned_data['ruta'].name
            tipo = formulario.cleaned_data['tipoDataset']
            nombreD = formulario.cleaned_data['nombreDataset']
            formatoImagen = formulario.cleaned_data['formatoImg']
            Zip.descomprimir(str(formulario.instance.ruta.name), rutaName, tipo, nombreD, formatoImagen)
            messages.success(request, f'Dataset {nombreD} creado correctamente')
            return redirect('datasets')
    else:
        formulario = DatasetForm()
    return render(request, 'datasets/crear.html', {'formulario': formulario})

def verDataset(request, id_Dataset):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    rutaDataset = '/datasets/'+dataset.ruta.name+'/entrenamiento/'
    dirsTrain = os.listdir(dataset.ruta.name+'/entrenamiento')
    return render(request, 'datasets/ver.html', {'imagenesEntrenamiento': dirsTrain, 'dataset': rutaDataset})

def editarDataset(request, id_Dataset):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    formulario = DatasetForm(request.POST or None, request.FILES or None, instance=dataset)
    if formulario.is_valid():
        nombre = formulario.cleaned_data['nombreDataset']
        messages.success(request, f'Dataset {nombre} modificado correctamente')
        formulario.save()
        return redirect('datasets')
    return render(request, 'datasets/editar.html', {'formulario': formulario, 'dataset': dataset})

def eliminarDataset(request, id_Dataset):
    dataset = Dataset.objects.get(id_Dataset=id_Dataset)
    dataset.delete()
    return redirect('datasets')