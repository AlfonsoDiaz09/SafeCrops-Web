from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from AppSafeCrops import views
from . import views
from django.urls import include, re_path, path
#from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.urls import static

#Crear la URL de la vista para conectar modelo vista controlador

urlpatterns = [
    path('login/', views.validation, name='login'), #URL de la vista de validacion de login
    path('password_Reset/', views.ResetPassword, name="passwordReset"), #URL de la vista de ingresar correo para recuperar contraseña
    path('send_email_reset/', views.sendEmail, name="sendEmailReset"), #URL que envia el correo para recuperar contraseña
    path('change_password<str:token>', views.ChangePassword, name="changePassword"), #URL de la vista de cambiar contraseña
    path('profile/', views.user_profile, name='profile'), #URL de la vista de perfil
    path('logout/', LogoutView.as_view(template_name="paginas/inicio.html"),name="salir"), #URL de la vista de logout

    path('', views.inicio, name='inicio'), # El nombre es para acceder a una url con ese nombre
    path('Panel_administrador', login_required(views.inicioA), name='inicioA'), #panel principal del administrador
    path('Panel_experto', login_required(views.inicioE), name='inicioE'), #panel principal del experto 
    path('Panel_tester', login_required(views.inicioT), name='inicioT'), #panel principal del tester

    path('administradores', login_required(views.administradores), name='administradores'), #consulta de administradores
    path('administrador/crear', login_required(views.crearAdministrador), name='crearA'), #crear administrador
    path('administrador/editar<str:id_Administrador>,<int:user_id>', login_required(views.editarAdministrador), name='editarA'), #editar administrador
    path('eliminar/<str:id_Administrador>', login_required(views.eliminarAdministrador), name='eliminarA'), #eliminar administrador

    path('expertos', login_required(views.expertos), name='expertos'), #consulta de expertos
    path('experto/crear', login_required(views.crearExperto), name='crearE'), #crear experto
    path('experto/editar<int:id_Experto>,<int:user_id>', login_required(views.editarExperto), name='editarE'), #editar experto
    path('eliminarE/<int:id_Experto>', login_required(views.eliminarExperto), name='eliminarE'), #eliminar experto

    path('testers', login_required(views.testers), name='testers'), #consulta de testers
    path('tester/crear', login_required(views.crearTester), name='crearT'), #crear tester
    path('tester/editar<int:id_Tester>,<int:user_id>', login_required(views.editarTester), name='editarT'), #editar tester
    path('eliminarT/<int:id_Tester>', login_required(views.eliminarTester), name='eliminarT'), #eliminar tester

    path('usuarios', login_required(views.usuarios), name='usuarios'), #consulta de usuarios
    # path('usuario/crear', views.crearUsuario, name='crearU'), #crear usuario
    # path('usuario/editar<int:id>', login_required(views.editarUsuario), name='editarU'), #editar usuario
    # path('eliminarU/<int:id>', login_required(views.eliminarUsuario), name='eliminarU'), #eliminar usuario

    path('enfermedades', login_required(views.enfermedades), name='enfermedades'), #consulta de enfermedades
    path('enfermedad/crear', login_required(views.crearEnfermedad), name='crearEnfermedad'), #crear enfermedad
    path('enfermedad/editar<int:id_Enfermedad>', login_required(views.editarEnfermedad), name='editarEnfermedad'), #editar enfermedad
    path('eliminarEnfermedad/<int:id_Enfermedad>', login_required(views.eliminarEnfermedad), name='eliminarEnfermedad'), #eliminar enfermedad

    path('datasets', login_required(views.datasets), name='datasets'), #consulta de datasets
    path('dataset/crear', login_required(views.crearDataset), name='crearDataset'), #crear dataset
    path('dataset/ver<int:id_Dataset>', login_required(views.verDataset), name='verDataset'), #ver dataset
    path('dataset/editar<int:id_Dataset>', login_required(views.editarDataset), name='editarDataset'), #editar dataset
    path('eliminarDataset/<int:id_Dataset>', login_required(views.eliminarDataset), name='eliminarDataset'), #eliminar dataset

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL_DATASET, document_root=settings.MEDIA_ROOT)
