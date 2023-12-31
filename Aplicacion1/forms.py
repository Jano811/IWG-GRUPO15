from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import preguntas, respuestas, preguntasrespondidas #sin ninguna funcion por ahora

class NewRegister(UserCreationForm):
    email= forms.EmailField(required=True)    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2'] #register pide esos datos
    
    
    def clean_email(self):  #revision y aviso de correo ya usado
        email=self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('correo ya en uso')
        return email

class ElegirUnaRespuestaCorrecta(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirUnaRespuestaCorrecta, self).clean()

        respuesta_correcta = 0
        for formulario in self.forms:         #si en el admin de django marcas 2 correctas el ciclo itera 2 veces 
            if not formulario.is_valid():     #por lo tanto respuesta_correcta = 2
                return                        
            
            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1
        try:
            assert respuesta_correcta == preguntas.num_respuestas_correctas    #si respuesta_correcta no es igual a la variable de respuestas 
        except AssertionError:                                                 #correctas puesto en el modelo va a tirar error
            raise forms.ValidationError('Solo una respuesta es valida')
        

class RespuestaForm(forms.Form):
    respuesta_seleccionada = forms.ModelChoiceField(queryset=respuestas.objects.all(), empty_label=None)
