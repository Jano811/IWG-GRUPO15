from django.contrib import admin
from .models import preguntas, respuestas, preguntasrespondidas
from .forms import ElegirUnaRespuestaCorrecta

class ElegirRespuestaInline(admin.TabularInline):    #muestre en una tabla las respuestas
    model= respuestas
    can_delete=False    
    max_num=respuestas.max_respuesta    #max numero de respuestas para escribir 
    min_num=respuestas.max_respuesta
    formset = ElegirUnaRespuestaCorrecta  #max numero de respuestas correctas de cada pregunta
class PreguntaAdmin(admin.ModelAdmin):
    model= respuestas
    inlines=(ElegirRespuestaInline, )  
    list_display = ['texto',]
    search_fields = ['texto' 'preguntas__texto']  

class preguntasrespondidasAdmin(admin.ModelAdmin):            #campos a mostrar
    list_display=['pregunta','respuestas','correcta','puntaje_obtenido']

    class Meta:
        model= preguntasrespondidas


admin.site.register(preguntasrespondidas)
admin.site.register(preguntas,PreguntaAdmin)
admin.site.register(respuestas)
