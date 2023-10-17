from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class preguntas(models.Model):   #creacion de preguntas

    texto=models.TextField(verbose_name='texto de pregunta')

    def __str__(self):
        return self.texto
    

class respuestas(models.Model):   #creacion de las respuestas


    max_respuesta=4   #maximo numero de respuestas a escribir
    pregunta = models.ForeignKey(preguntas, related_name='preguntas', on_delete=models.CASCADE)
    correcta= models.BooleanField(verbose_name='marcar si es la respuesta correcta', default=False, null=False)
    texto= models.TextField(verbose_name='Texto de la respuesta')


    def __str__(self):
        return self.texto


class Usuario(models.Model):     #saber quien respondio
    usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    puntajetotal= models.DecimalField(verbose_name='puntaje total',default=0,decimal_places=2,max_digits=10)

class preguntasrespondidas(models.Model):       #guarda las preguntas respondidas
    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)  #por si acaso si el null no existe genera error al ya existir una base de datos e intentar modificarla despues
    pregunta= models.ForeignKey(preguntas, on_delete=models.CASCADE)
    respuestas=models.ForeignKey(respuestas, on_delete=models.CASCADE,related_name='intentos')
    correcta=models.BooleanField('es esta la respuesta correcta?',default=False,null=False)
    puntaje_obtenido=models.DecimalField(verbose_name='Puntaje',default=0,decimal_places=2,max_digits=6)

