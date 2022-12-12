from django.shortcuts import render, redirect
from django.http import HttpResponse
from compra.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

#login
from compra.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

def Inicio (request):
    return render(request, "compra/inicio.html")

def Nosotros (request):
    return render(request, "compra/Nosotros.html")
#def Automovil(request):
#    return render(request, "compra/Automovil.html")

#def Clientes(request):
    #return render(request, "compra/Clientes.html")
 
class AutomovilList(ListView):
    model = Rodado
    template_name = "compra/list_automovil.html"


class AutomovilDetail(DetailView):
    model = Rodado
    template_name = "compra/detail_automovil.html"

class AutomovilCreate(CreateView):
    model = Rodado
    success_url = "/compra/automovil/"
    fields = ["marca", "modelo" , "color", "km", "año", "precio", "patente", "vtv_hecha"]
    template_name = "compra/rodado_form.html"
    
class AutomovilUpdate(UpdateView):
    model = Rodado
    success_url = "/compra/automovil/"
    fields = ["marca", "modelo" , "color", "km", "año", "precio", "patente", "vtv_hecha"]

class AutomovilDelete(DeleteView):
    model = Rodado  
    success_url = "/compra/automovil/"



class Auto_BuscadoList(ListView):
    model = Auto_Buscado
    template_name = "compra/list_Auto_Buscado.html"

class Auto_BuscadoDetail(DetailView):
    model = Auto_Buscado
    template_name = "compra/detail_Auto_Buscado.html"

class Auto_BuscadoCreate(CreateView):
    model = Auto_Buscado
    success_url = "/compra/Auto_Buscado/"
    fields = [ "marca" , "modelo" , "color" , "nombre_comprador", "apellido" , "dni", "celular", "email"]
    template_name = "compra/Auto_Buscado_form.html"
    
class Auto_BuscadoUpdate(UpdateView):
    model = Auto_Buscado
    success_url = "/compra/Auto_Buscado/"
    fields = ["nombre", "apellido" , "dni", "domicilio", "localidad", "celular", "email"]

class Auto_BuscadoDelete(DeleteView):
    model = Auto_Buscado
    success_url = "/compra/vendedor/"




#aseguradora 
class AseguradoraList(ListView):
    model = Aseguradora
    template_name = "compra/list_aseguradora.html"

class AseguradoraDetail(DetailView):
    model = Aseguradora
    template_name = "compra/detail_aseguradora.html"

class AseguradoraCreate(CreateView):
    model = Aseguradora
    success_url = "/compra/aseguradora/"
    fields = ["razon_social", "telefono" , "celular", "poliza", "domicilio", "localidad"]
    template_name = "compra/aseguradora_form.html"
    
class AseguradoraUpdate(UpdateView):
    model = Aseguradora
    success_url = "/compra/aseguradora/"
    fields = ["razon_social", "telefono" , "celular", "poliza", "domicilio", "localidad"]

class AseguradoraDelete(DeleteView):
    model = Aseguradora
    success_url = "/compra/aseguradora/"

    

#inicio de sesion
def iniciar_sesion(request):

    errors = ""

    if request.method == "POST":
        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data

            user = authenticate(username=data["username"], password=data["password"])
            
            if user is not None:
                login(request, user)
                return redirect ("compra-inicio")
            else:
                return render(request, "compra/login.html", {"form": formulario, "errors": "Credenciales invalidas"})
        else:
            return render(request, "compra/login.html", {"form": formulario, "errors": formulario.errors})
    formulario = AuthenticationForm()
    return render(request, "compra/login.html", {"form": formulario, "errors": errors})

    
def registrar_usuario(request):

    if request.method == "POST":
        formulario = UserRegisterForm(request.POST)

        if formulario.is_valid():
            
            formulario.save()
            return redirect("compra-inicio")
        else:
            return render(request, "compra/register.html", { "form": formulario, "errors": formulario.errors})

    formulario  = UserRegisterForm()
    return render(request, "compra/register.html", { "form": formulario})

@login_required
def editar_perfil(request):

    usuario = request.user

    if request.method == "POST":
        # * cargar informacion en el formulario
        formulario = UserEditForm(request.POST)

        # ! validacion del formulario
        if formulario.is_valid():
            data = formulario.cleaned_data

            # * actualizacion del usuario con los datos del formulario
            usuario.email = data["email"]
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]

            usuario.save()
            return redirect("compra-inicio")
        else:
            return render(request, "compra/editar_perfil.html", {"form": formulario, "erros": formulario.errors})
    else:
        # * crear formulario vacio
        formulario = UserEditForm(initial = {"email": usuario.email, "first_name": usuario.first_name, "last_name": usuario.last_name})

    return render(request, "compra/editar_perfil.html", {"form": formulario})
