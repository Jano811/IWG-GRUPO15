from django.shortcuts import render, redirect,get_object_or_404
from .forms import NewRegister, UsuarioForm
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
            region = user_creation_form.cleaned_data.get('region')   #almacena el registro de comuna y region 
            comuna = user_creation_form.cleaned_data.get('comuna')
            birth_date = user_creation_form.cleaned_data.get('birth_date')
            gender = user_creation_form.cleaned_data.get('gender')
            user=authenticate(username=user_creation_form.cleaned_data['username'],password=user_creation_form.cleaned_data['password1'])
            usuario = Usuario.objects.create(usuario=user, region=region, comuna=comuna, birth_date=birth_date,gender=gender)  #muestra el campo relleno de region y comuna
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
def nosotros(request):
    return render(request,'nosotros.html')

@login_required
def inicio(request):
    return render(request,'inicio.html')

@login_required
def psd(request):
    qusuario, created = Usuario.objects.get_or_create(usuario=request.user)  
    if request.method == 'POST':                        #se manda a la base la respuesta marcada y verifica si es correcta o no 
        pregunta_pk = request.POST.get('pregunta_pk')
        respuesta_pk = request.POST.get('respuesta_pk')
        print(f"pregunta_pk: {pregunta_pk}")
        if not pregunta_pk or not respuesta_pk:
            return HttpResponseBadRequest("Porfavor responda a la pregunta, vuelva atras")

        prespondida, created = PreguntasRespondidas.objects.get_or_create(quizuser=qusuario,pregunta=pregunta_pk)

        # Obtener la respuesta seleccionada
        opcionselect = get_object_or_404(respuestas, pk=respuesta_pk)

        # Asignar la respuesta seleccionada y guardar
        prespondida.respuesta = opcionselect
        prespondida.correcta = opcionselect.correcta
        prespondida.puntaje_obtenido = opcionselect.pregunta.max_puntaje if opcionselect.correcta else 0
        prespondida.save()
        qusuario.intento_valido(prespondida, opcionselect)  #llama a intento valido para sumar puntos totales en el perfil
        return redirect('retroalimentacion_url', prespondida.pk)   

    else:

        pregunta=qusuario.nuevas_preguntas()
        if pregunta is not None:
            qusuario.fintentos(pregunta)
            
        context = {'pregunta': pregunta}  
    return render(request, 'psd.html', context)


@login_required
def resultadospregunta(request, prespondida_pk):           #proporciona los datos para poder mostrar los resultados en la retroalimentacion               
    respondida = get_object_or_404(PreguntasRespondidas, pk=prespondida_pk)
    retroalimentacion = respondida.pregunta.retroalimentacion
        
    context = {
        'respondida': respondida,
        'retroalimentacion_pregunta': retroalimentacion,
    }
    return render(request, 'retroalimentacion.html', context)

@login_required
def perfil(request):
    usuario = request.user
    return render(request, 'perfil.html', {'usuario': usuario})

def editarperfil(request):
    usuario = request.user

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil') 
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'editarperfil.html', {'form': form})