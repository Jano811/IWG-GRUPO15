from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewRegister, RespuestaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import preguntas, respuestas, Usuario, preguntasrespondidas
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
import pdb



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

#para que una view necesite haber iniciado sesion para entrar y no se evada entrando directo desde el link 
#necesita el @login_required antes
@login_required    
def cuestionario(request):
    return render(request,'cuestionario.html')

@login_required
def inicio(request):
    return render(request,'inicio.html')

@login_required
def psd(request):
    usuario, created = Usuario.objects.get_or_create(usuario=request.user)
    nueva_pregunta = usuario.nuevas_preguntas()

    opciones_respuesta = nueva_pregunta.opciones.all()
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta_seleccionada = form.cleaned_data['respuesta_seleccionada']
            pregunta_respondida, created = preguntasrespondidas.objects.get_or_create(quizuser=usuario, pregunta=nueva_pregunta, defaults={'respuesta': respuesta_seleccionada})
            if not created:
                pregunta_respondida.respuesta = respuesta_seleccionada
                pregunta_respondida.save()
                usuario.save()
                
            # Redirige a la retroalimentación después de responder cada pregunta
            return redirect('retroalimentacion_url') #, pregunta_respondida.pk
        
    else:
        form = RespuestaForm()

    context = {
        'pregunta': nueva_pregunta,
        'opciones_respuesta': opciones_respuesta,
        'form': form,
    }

    return render(request, 'psd.html', context)


@login_required
def retroalimentacion(request):
	return render(request, 'retroalimentacion.html')

