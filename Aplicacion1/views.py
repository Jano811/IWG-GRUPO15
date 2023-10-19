from django.shortcuts import render, redirect
from .forms import NewRegister
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def iniciodesesion(request):
    return render(request,'iniciodesesion.html')

def login_user(request): #cambio de login a login_user, al confundirse con la variable login del register
    return redirect(request, 'inicio.html')

def register(request):  #formulario de registro, se guarda en la base de datos
    data = {
        'form' : NewRegister()
    }
    if request.method == 'POST' :
        user_creation_form = NewRegister(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user=authenticate(username=user_creation_form.cleaned_data['username'],password=user_creation_form.cleaned_data['password1'])
            login(request,user)  
            return redirect('iniciodesesion')
        else:
            data['form']=user_creation_form    #no borra los datos si son incorrectos
    return render(request, 'registration/register.html',data)


def psd(request): #no funciona?
    return render(request,'psd.html')
    
def cuestionario(request):
    return render(request,'cuestionario.html')



@login_required
def inicio(request):#posible problema
    return render(request,'inicio.html')
