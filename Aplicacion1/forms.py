from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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