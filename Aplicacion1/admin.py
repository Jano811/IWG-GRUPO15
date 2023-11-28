from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import preguntas, respuestas, PreguntasRespondidas, Usuario
from django.contrib.auth.models import User
from .forms import ElegirUnaRespuestaCorrecta

class UsuarioInline(admin.StackedInline):  
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Datos del Usuario'
    fields = ('region', 'comuna','birth_date','gender')

class UserAdmin(BaseUserAdmin):  #usuarioinline y useradmin personalizan la interfaz del admin con informacion del modelo Usuario
    inlines = (UsuarioInline,)

class ElegirRespuestaInline(admin.TabularInline):    #muestre en una tabla las respuestas
    model= respuestas
    can_delete=False    
    max_num=respuestas.max_respuesta    #max numero de respuestas para escribir 
    min_num=respuestas.max_respuesta
    formset = ElegirUnaRespuestaCorrecta  #max numero de respuestas correctas de cada pregunta

class PreguntaAdmin(admin.ModelAdmin):
    model= respuestas
    inlines=(ElegirRespuestaInline, )  
    list_display = ['texto']
    search_fields = ['texto' 'preguntas__texto']  

class preguntasrespondidasAdmin(admin.ModelAdmin):            
    list_display=['pregunta','respuestas','correcta','puntaje_obtenido'] #campos a mostrar

    class Meta:
        model= PreguntasRespondidas

admin.site.unregister(User)  #para que muestre un modelo personalizado del usuario.
admin.site.register(User, UserAdmin)
admin.site.register(PreguntasRespondidas)
admin.site.register(preguntas,PreguntaAdmin)
admin.site.register(respuestas)
admin.site.register(Usuario)
