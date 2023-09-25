from django.shortcuts import render, redirect
from .forms import NewRegister
from django.contrib.auth.decorators import login_required
# Create your views here.

def iniciodesesion(request):
    return render(request,'iniciodesesion.html')

def login(request):
    return redirect(request, 'inicio.html')

def register(request):
    data = {
        'form' : NewRegister()
    }
    if request.method == 'POST' :
        user_creation_form = NewRegister(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('inicio')
    return render(request, 'registration/register.html',data)


@login_required
def inicio(request):
    return render(request,'inicio.html')
