from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from .users import *
from .models import Mascota, Asesor
from django.http import Http404
from django.urls import reverse
from .form import MascotaForm, UserRegistrationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


def index(request):
    template_name = 'index.html'
    mascotas = Mascota.objects.all()
    context = {'mascotas': mascotas
               }
    return render(request, template_name, context)


def signup(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form': form})

    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Asignar grupo seleccionado
            group = form.cleaned_data['group']
            group.user_set.add(user)

            # Iniciar sesión automáticamente después del registro (opcional)
            login(request, user)
            return redirect('dashboard')

        return render(request, 'signup.html', {'form': form, 'error': 'Error al registrar el usuario.'})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El Usuario o la Contraseña esta incorrecta'
            })
        else:
            login(request, user)

            # Redirección basada en roles
            if user.is_superuser:
                return redirect('admin_dashboard')  # Vista o URL del administrador
            elif user.groups.filter(name='Asesor de Tienda').exists():
                return redirect('dashboard')  # Vista o URL del asesor
            else:
                return redirect('default_dashboard')  # Redirección genérica en caso de no pertenecer a ningún rol específico
             
def signout(request):
    logout(request)
    return redirect('index')

def user_dashboard(request):
    template_name = 'default_dashboard.html'
    mascotas = Mascota.objects.all()
    context = {'mascotas': mascotas
               }
    return render(request, template_name, context)

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def dashboard(request):
    return render(request, 'dashboard.html') # Retorna el dashborad del asesor

def grabar_mascotas(request):
    context = {}
    template_name = "grabar_mascotas.html"
    
    # Solo permitir agregar mascotas si el usuario está autenticado
    if request.user.is_authenticated:
        if request.method == "POST":
            form = MascotaForm(request.POST, request.FILES)  # Incluye request.FILES para manejar imágenes
            if form.is_valid():
                raza = form.cleaned_data.get("raza")
                tamaño = form.cleaned_data.get("tamaño")
                descripcion = form.cleaned_data.get("descripcion")
                
                # Obtén el asesor relacionado con el usuario autenticado
                asesor = request.user.asesor  # Relacionamos al asesor del usuario autenticado

                # Crear una nueva instancia de la mascota
                mascota = Mascota.objects.create(
                    raza=raza,
                    tamaño=tamaño,
                    asesor=asesor,  # Relacionamos la mascota con el asesor
                    descripcion=descripcion,
                    foto=form.cleaned_data.get('foto')  # Si el formulario incluye un campo de foto
                )
                mascota.save()
                return redirect('listar_mascotas')  # Redirigir a la lista de mascotas (cambia a la URL que uses)
        
        else:
            form = MascotaForm()

        context['form'] = form
        return render(request, template_name, context)
    else:
        return redirect('signin')


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
