from django.contrib import admin
from .models import Administrador, Experto, Tester


# Register your models here.

'''
Se registran los modelos para que aparezcan en el panel de administración de django
'''
admin.site.register(Administrador)
admin.site.register(Experto)
admin.site.register(Tester)