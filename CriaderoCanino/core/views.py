from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from .users import *
from .models import Mascota, Asesor
from django.http import Http404
from django.urls import reverse
from .form import MascotaForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.db import IntegrityError


def index(request):
    template_name = 'index.html'
    mascotas = Mascota.objects.all()
    context = {'mascotas': mascotas
               }
    return render(request, template_name, context)


def signup(request):

    if request.method == 'GET':

        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'La contra no coincide'
        })


def signout(request):
    logout(request)
    return redirect('index')


def dashboard(request):
    return render(request, 'dashboard.html')

def signin(request):
    return render(request, 'signin.html')


def grabar_mascotas(request):
    context = {}
    template_name = "grabar_mascotas.html"
    if request.method == "POST":
        form = MascotaForm(request.POST)
        if form.is_valid():
            raz = form.cleaned_data.get("raza")
            tam = form.cleaned_data.get("tamaño")
            ase = form.cleaned_data.get("asesor")
            des = form.cleaned_data.get("descripcion")
            obj = Mascota.objects.create(
                raza=raz,
                tamaño=tam,
                asesor=ase,
                descripcion=des
            )
            obj.save()

    else:
        form = MascotaForm()
    context['form'] = form
    return render(request, template_name, context)


def listado_mascotas(request):
    template_name = "Listado_mascotas.html"
    return render(request, template_name)


def mascota(request, masctota_id):
    template_name = 'mascota.html'
    try:
        mascota = Mascota.objects.get(pk=masctota_id)
    except Mascota.DoesNotExist:
        raise Http404("Mascota no existe")
    context = {
        "mascota": mascota,
        # intentar incluir el asesor posible con get
        "no_asesor": Asesor.objects.exclude(mascota=mascota).all()

    }
    return render(request, template_name, context)


def comprar(request, mascota_id):
    try:
        template_name = 'index.html'
        cliente_id = request.POST["cliente"]
        cliente = Asesor.objects.get(pk=cliente_id)
        mascota = Mascota.objects.get(pk=mascota_id)
    except KeyError:
        print("No selecciono Asesor")
    except Mascota.DoesNotExist:
        print("La mascota no existe")
    except Asesor.DoesNotExist:
        print("El asesor no existe")

    cliente.mascota.add(mascota)
    mascota.comprado = cliente.nombre
    mascota.save()

    return HttpResponseRedirect(reverse("mascota", args=(mascota_id,)))


def ListarUsuarios(request):
    users = User.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios':
                                                    users})


def CrearUsuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        phone = request.POST['phone']
        is_boss = request.POST['is_boss']
        user = User(email=email, name=name, password=password,
                    phone=phone, is_boss=is_boss)
    if email.is_valid():
        user.save()
        return redirect('listar_usuarios')
    else:
        return render(request, 'crear_usuario.html')


def EditarUsuario(request, email):
    user = User.objects.get(email=email)
    if request.method == 'GET':
        return render(request, 'editar_usuario.html', {'usuario': user})
    else:
        user.email = request.POST['email']
        user.name = request.POST['name']
        user.password = request.POST['password']
        user.phone = request.POST['phone']
        user.is_boss = request.POST['is_boss']
        user.save()
    return redirect('listar_usuarios')


def EliminarUsuario(request, email):
    user = User.objects.get(email=email)
    if request.method == 'POST':
        user.delete()
        return redirect('listar_usuarios')
    else:
        return render(request, 'eliminar_usuario.html', {'usuario': user})
