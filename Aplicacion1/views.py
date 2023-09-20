from django.shortcuts import render, redirect
from .forms import NewRegister
from django.contrib.auth.decorators import login_required
# Create your views here.

def iniciodesesion(request):
    return render(request,'iniciodesesion.html')

def login(request):
    return redirect(request, 'inicio.html')
def register(request):
    if request.method == "POST":
        form = NewRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
        else:
            form = NewRegister()
    return render(request, 'registration/register.html',{'form':NewRegister})


@login_required
def inicio(request):
    return render(request,'inicio.html')
