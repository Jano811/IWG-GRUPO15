from django.shortcuts import render, redirect,get_object_or_404
from .forms import NewRegister#,RespuestaForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Usuario, PreguntasRespondidas,respuestas
from django.http import HttpResponseBadRequest 




def iniciodesesion(request):
    return render(request,'iniciodesesion.html')

def login_user(request): #cambio de login a login_user, al confundirse con la variable login del register,,,,,creo que la funcion no hace nada
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
            data['form']=user_creation_form    #no borra todos los datos si se pone algo incorrecto
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
    qusuario, created = Usuario.objects.get_or_create(usuario=request.user)  
    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        respuesta_pk = request.POST.get('respuesta_pk')
        print(f"pregunta_pk: {pregunta_pk}")
        if not pregunta_pk or not respuesta_pk:
            return HttpResponseBadRequest("El identificador de la pregunta no se proporcionó correctamente.")

        prespondida, created = PreguntasRespondidas.objects.get_or_create(quizuser=qusuario,pregunta=pregunta_pk)

        # Obtener la respuesta seleccionada
        opcionselect = get_object_or_404(respuestas, pk=respuesta_pk)

        # Asignar la respuesta seleccionada y guardar
        prespondida.respuesta = opcionselect
        prespondida.correcta = opcionselect.correcta
        prespondida.puntaje_obtenido = opcionselect.pregunta.max_puntaje if opcionselect.correcta else 0
        prespondida.save()

        return redirect('retroalimentacion_url', prespondida.pk)   

    else:

        pregunta=qusuario.nuevas_preguntas()
        if pregunta is not None:
            qusuario.fintentos(pregunta)
            
        context = {'pregunta': pregunta}  
    return render(request, 'psd.html', context)

def resultadospregunta(request, prespondida_pk):
	respondida = get_object_or_404(PreguntasRespondidas, pk=prespondida_pk)
    
	context = {
		'respondida':respondida
	}
	return render(request, 'retroalimentacion.html', context)



@login_required
def retroalimentacion(request):
	return render(request, 'retroalimentacion.html')

