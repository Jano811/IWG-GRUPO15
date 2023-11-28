from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import preguntas, Usuario

class NewRegister(UserCreationForm):
    email= forms.EmailField(required=True)   
    region = forms.CharField(max_length=40, required=False)  #campo de region y comuna en el registro
    comuna = forms.CharField(max_length=40, required=False)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Utiliza un widget de fecha
        required=False
    )
    gender = forms.CharField(max_length=40, required=False)

    class Meta:
        model=User
        fields=['username','first_name','last_name', 'email', 'password1', 'password2', 'region', 'comuna', 'birth_date', 'gender'] #register pide esos datos
        widgets = {
        'username': forms.TextInput(attrs={'autocomplete': 'off'}),
    }
    
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
        

class UsuarioForm(forms.ModelForm):  #para cambiar los datos del perfil
    class Meta:
        model = Usuario
        fields = ['region', 'comuna','birth_date', 'gender'] 
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        } 

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(label='Fecha de nacimiento')
    gender = forms.CharField(label='Género')

    class Meta(UserCreationForm.Meta):
        # Puedes añadir más configuraciones si es necesario
        pass