
from base64 import urlsafe_b64decode
import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required 
from .models import Administrador, Experto, Tester, Enfermedad, Dataset, Usuario
from .forms import AdministradorForm, ExpertoForm, TesterForm, UsuarioForm, ResetPasswordForm, ChangePasswordForm, EnfermedadForm, DatasetForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from .zip import Zip
import mysql.connector
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
            context={
                'mail':mail, 
                'user':user,
                'link_resetpwd': 'http://{}/change_password{}'.format(URL, str(user.token)),
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

    for user in queryEmailExperto:
        if mail == user.correo:
            print("Enviar correo a", mail)
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            print("Usuario ", user)
            print("Prueba ", user.nombre)
            print("Token ", user.token)
            user.save()
            context={
                'mail':mail, 
                'user':user,
                'link_resetpwd': 'http://{}/change_password{}'.format(URL, str(user.token)),
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

    for user in queryEmailTester:
        if mail == user.correo:
            print("Enviar correo a", mail)
            URL = settings.DOMAIN if not settings.DEBUG else request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            print("Usuario ", user)
            print("Prueba ", user.nombre)
            print("Token ", user.token)
            user.save()
            context={
                'mail':mail, 
                'user':user,
                'link_resetpwd': 'http://{}/change_password{}'.format(URL, str(user.token)),
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
    usuariosAdmin = Administrador.objects.all()
    usuariosExperto = Experto.objects.all()
    usuariosTester = Tester.objects.all()
    bandera = False
    
    for user in usuariosAdmin:
        if User.objects.filter(token=token).exists():
            bandera = True
    for user in usuariosExperto:
        if User.objects.filter(token=token).exists():
            bandera = True
    for user in usuariosTester:
        if User.objects.filter(token=token).exists():
            bandera = True
    
    if bandera == False:
        messages.error(request, f'El token no existe en la base de datos')
    elif bandera == True:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(request, f'Contraseña cambiada correctamente')
                return redirect('login/')
            else:
                form = ChangePasswordForm()
            return render(request, 'registration/change_pwd.html', {'form': form_class})

def ChangePassword(request, token):
    form_class = ChangePasswordForm(request.POST or None)
    usuariosAdmin = Administrador.objects.all()
    usuariosExperto = Experto.objects.all()
    usuariosTester = Tester.objects.all()
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
        return render(request, 'registration/change_pwd.html', {'form': form_class})


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


#*****************************************************************************************************#
#*****************************************************************************************************#
#**********                       GESTIÓN DE USUARIOS ADMINISTRADORES                       **********#
#*****************************************************************************************************#
#*****************************************************************************************************#

def administradores(request): #función para redireccionar a la página donde se enlista todos los administradores
    administradores = Administrador.objects.all()
    return render(request, 'usuarios/administrador/indexA.html', {'administradores': administradores})

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
    else: # Si no se ha enviado el formulario
        formularioUsuario = UsuarioForm()
        formularioAdministrador = AdministradorForm()
        #formularioUsuario = UsuarioForm(instance=request.user)
        #formularioAdministrador = AdministradorForm(instance=request.user.administradorUser)
    return render(request, 'usuarios/administrador/crear.html', {'formularioUsuario': formularioUsuario, 'formularioAdministrador': formularioAdministrador})

def editarAdministrador(request, id_Administrador, user_id): #función para editar un administrador con parametros de matricula
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
         
    return render(request, 'usuarios/administrador/editar.html', {'formularioAdministrador': formularioAdministrador, 'formularioUsuario':formularioUsuario, 'administrador': administrador, 'usuario': usuario})

def eliminarAdministrador(request, id_Administrador): #función para eliminar un administrador con parametros de matricula
    administrador = Administrador.objects.get(id_Administrador=id_Administrador)
    usuario = User.objects.get(id=administrador.user_id)
    administrador.delete()
    usuario.delete()
    return redirect('administradores')


#*****************************************************************************************************#
#*****************************************************************************************************#
#**********                           GESTIÓN DE USUARIOS EXPERTOS                          **********#
#*****************************************************************************************************#
#*****************************************************************************************************#

def expertos(request): #función para redireccionar a la página donde se enlista todos los expertos
    expertos = Experto.objects.all()
    return render(request, 'usuarios/experto/indexE.html', {'expertos': expertos})

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
    else: # Si no se ha enviado el formulario
        formularioUsuario = UsuarioForm()
        formularioExperto = ExpertoForm()
    return render(request, 'usuarios/experto/crear.html', {'formularioUsuario': formularioUsuario, 'formularioExperto': formularioExperto})

def editarExperto(request, id_Experto, user_id): #función para editar un administrador con parametros de matricula
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
         
    return render(request, 'usuarios/experto/editar.html', {'formularioExperto': formularioExperto, 'formularioUsuario':formularioUsuario, 'experto': experto, 'usuario': usuario})

def eliminarExperto(request, id_Experto):
    experto = Experto.objects.get(id_Experto=id_Experto)
    usuario = User.objects.get(id=experto.user_id)
    experto.delete()
    usuario.delete()
    return redirect('expertos')


#*****************************************************************************************************#
#*****************************************************************************************************#
#**********                           GESTIÓN DE USUARIOS TESTERS                           **********#
#*****************************************************************************************************#
#*****************************************************************************************************#

def testers(request): #función para redireccionar a la página donde se enlista todos los testers
    testers = Tester.objects.all()
    return render(request, 'usuarios/tester/indexT.html', {'testers': testers})

def crearTester(request): #función para crear un nuevo éxperto
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
    return render(request, 'usuarios/tester/crear.html', {'formularioUsuario': formularioUsuario, 'formularioTester': formularioTester})

def editarTester(request, id_Tester, user_id): #función para editar un administrador con parametros de matricula
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
         
    return render(request, 'usuarios/tester/editar.html', {'formularioTester': formularioTester, 'formularioUsuario':formularioUsuario, 'tester': tester, 'usuario': usuario})

def eliminarTester(request, id_Tester): #función para eliminar un tester con parametros de matricula
    tester = Tester.objects.get(id_Tester=id_Tester) #se obtiene el tester con la matricula
    usuario = User.objects.get(id=tester.user_id) #se obtiene el usuario del tester
    tester.delete() #se elimina el tester
    usuario.delete() #se elimina el usuario
    return redirect('testers') #se redirecciona a la página de testers


#*****************************************************************************************************#
#*****************************************************************************************************#
#**********                          GESTIÓN DE PERFIL DE USUARIOS                          **********#
#*****************************************************************************************************#
#*****************************************************************************************************#

def usuarios(request): #función para redireccionar a la página donde se enlista todos los usuarios
    usuarios = User.objects.all()
    return render(request, 'usuarios/usuario/indexU.html', {'usuarios': usuarios})

def eliminarUsuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('usuarios')


#*****************************************************************************************************#
#*****************************************************************************************************#
#**********                             GESTIÓN DE ENFERMEDADES                             **********#
#*****************************************************************************************************#
#*****************************************************************************************************#

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


#*****************************************************************************************************#
#*****************************************************************************************************#
#**********                               GESTIÓN DE DATASETS                               **********#
#*****************************************************************************************************#
#*****************************************************************************************************#

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