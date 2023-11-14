from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import random

class preguntas(models.Model):   #creacion de preguntas

    num_respuestas_correctas = 1  #cuantas respuestas correctas van a tener las preguntas

    texto = models.TextField(verbose_name='texto de pregunta')
    max_puntaje = models.DecimalField(verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)
    def __str__(self):
        return self.texto
    

class respuestas(models.Model):   #creacion de las respuestas

    max_respuesta=4   #maximo numero de respuestas a escribir

    pregunta = models.ForeignKey(preguntas, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name='marcar si es la respuesta correcta', default=False, null=False)
    texto = models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.texto
    

class Usuario(models.Model):     #saber quien respondio
    usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    puntajetotal= models.DecimalField(verbose_name='puntaje total',default=0,decimal_places=2,max_digits=10)

    def intentos(self, pregunta):
        intento  = preguntasrespondidas(pregunta=pregunta, quizuser = self)
        intento.save()

    def nuevas_preguntas(self):
        respondidas = preguntasrespondidas.objects.filter(quizuser=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes = preguntas.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)

    def intento_valido(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta != respuesta_seleccionada.pregunta:
            return
        
        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_seleccionada

        else:
            pregunta_respondida.correcta = False
            pregunta_respondida.respuesta = respuesta_seleccionada

        pregunta_respondida.save() 
        self.actualizar_puntaje()

    def actualizar_puntaje(self):
    # Filtrar preguntas respondidas del usuario actual
        preguntas_respondidas = preguntasrespondidas.objects.filter(quizuser=self)
    # Filtrar las preguntas respondidas que son correctas
        preguntas_correctas = preguntas_respondidas.filter(correcta=True)
    # Calcular el puntaje total sumando los puntajes obtenidos de las preguntas correctas
        puntaje_actualizado = preguntas_correctas.aggregate(models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']
    # Actualizar el puntaje total del usuario
        self.puntajetotal = puntaje_actualizado
        self.save()


class preguntasrespondidas(models.Model):       #guarda las preguntas respondidas
    quizuser = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, related_name='intentos')  #por si acaso si el null no existe genera error al ya existir una base de datos e intentar modificarla despues
    pregunta = models.ForeignKey(preguntas, on_delete=models.CASCADE)
    respuesta =models.ForeignKey(respuestas, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(verbose_name='es esta la respuesta correcta?',default=False,null=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje',default=0,decimal_places=2,max_digits=6)


