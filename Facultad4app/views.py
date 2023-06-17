from django.shortcuts import render, redirect
from .models import Bonificacion, Dieta, Expediente, Prestamo, User
from .forms import BonificacionForm, DietaForm, ExpedienteForm, PrestamoForm, UserAddForm, UserEditForm
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout, login, authenticate



# Create your views here.


def create_user_default():
    if not User.objects.filter(username='Secretaria').exists():
        User.objects.create_user(username='Secretaria', name='Secretaria', last_name='Secretaria', role='Secretaria', password='12345678')
    if not User.objects.filter(username='Vicedecano').exists():
        User.objects.create_user(username='Vicedecano', name='Vicedecano', last_name='Vicedecano', role='Vicedecano', password='12345678')
    if not User.objects.filter(username='Administrador').exists():
        User.objects.create_user(username='Administrador', name='Administrador', last_name='Administrador', role='Administrador', password='12345678')    

def auth_login(request):
    create_user_default()
    if request.GET.get('next', False) and request.GET.get('next') != '/': 
        messages.error(request, 'No tiene los permisos necesarios para ejecutar esta acción, por favor inicie sesión', 'alert alert-danger alert-lng')
    if request.method == 'POST':
        user_test = User.objects.filter(username=request.POST['username'])
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('Inicio')
        else:
            messages.error(request, 'Credenciales Incorrectas', 'alert alert-danger alert-lng')
            return render(request, 'index.html')
    return render(request, 'index.html')

def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Ha cerrado sesión correctamente', 'alert alert-success alert-lng')
    return redirect('login')

@login_required(login_url=settings.LOGIN_URL)
def Bonificaciones(request): 
    bonificaciones = Bonificacion.objects.all()
    return render(request, "Bonificaciones.html", context = {'bonificaciones': bonificaciones})

@login_required(login_url=settings.LOGIN_URL)
def Crear_Bonificaciones(request):
    if request.method == 'POST': 
        form = BonificacionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if len(name) < 2:
                messages.warning(request, 'El nombre debe tener al menos 2 caracteres')
                bonificaciones = Bonificacion.objects.all()
            if starts_with_uppercase(name) == False:
                messages.warning(request, 'EL nombre no puede empezar con minúsculas')
                bonificaciones = Bonificacion.objects.all()
            lastname = form.cleaned_data.get('lastname')
            if starts_with_uppercase(lastname) == False:
                messages.warning(request, 'Los apellidos no puede empezar con minúsculas')
                bonificaciones = Bonificacion.objects.all()
            origen = form.cleaned_data.get('origen')
            if len(origen) < 2:
                messages.warning(request, 'El origen debe tener al menos 2 caracteres')
                bonificaciones = Bonificacion.objects.all()
            destino = form.cleaned_data.get('destino')
            if len(destino) < 2:
                messages.warning(request, 'El destino debe tener al menos 2 caracteres')
                bonificaciones = Bonificacion.objects.all()
            costo_Pasaje = form.cleaned_data.get('costo_Pasaje')
            if costo_Pasaje <= 0 :
                messages.warning(request, 'El costo del pasaje no puede ser negativo o cero')
                bonificaciones = Bonificacion.objects.all()
                
                return render(request, 'Bonificaciones.html', context= {'is_post': True, 'bonificaciones': bonificaciones, 
                    'name_f': request.POST['name'],
                    'lastname_f': request.POST['lastname'],
                    'origen_f': request.POST['origen'],
                    'destino_f': request.POST['destino'],
                    'CI_f': request.POST['CI'],
                    'costo_Pasaje_f': request.POST['costo_Pasaje'],
                    'fecha_f': request.POST['fecha'],
                })
            bonificacion = {
                'name': form.cleaned_data['name'],
                'lastname': form.cleaned_data['lastname'],
                'origen': form.cleaned_data['origen'],
                'destino': form.cleaned_data['destino'],
                'CI': form.cleaned_data['CI'],
                'fecha': form.cleaned_data['fecha'],
                'costo_Pasaje': form.cleaned_data['costo_Pasaje'],
            }
            Bonificacion.objects.create(**bonificacion)
            messages.success(request, 'Se ha agregado la bonificacion correctamente', 'alert alert-success')

            return redirect("Crear-Bonificacion")    
        else:
            messages.warning(request, 'Formulario inválido.')
            bonificaciones = Bonificacion.objects.all()
            return render(request, 'Bonificaciones.html', context= {'is_post': True, 'bonificaciones': bonificaciones, 
                'name_f': request.POST['name'],
                'lastname_f': request.POST['lastname'],
                'origen_f': request.POST['origen'],
                'destino_f': request.POST['destino'],
                'CI_f': request.POST['CI'],
                'costo_Pasaje_f': request.POST['costo_Pasaje'],
                'fecha_f': request.POST['fecha'],
            })
            
       # else:
           # print('Hola 3')
           # messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger')
            #bonificaciones = Bonificacion.objects.all()
            #return render(request, 'Bonificaciones.html', context= {'is_post': True, 'bonificaciones': bonificaciones})
    return redirect('Bonificaciones')

@login_required(login_url=settings.LOGIN_URL)
def editar_bonificacion(request, pk = None):
    o = Bonificacion.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado la bonificacion a modificar', 'alert alert-danger alert-lng')
        return redirect('Bonificaciones')
    o = o.first()
    if request.method == 'POST':
        form = BonificacionForm(request.POST)
        if form.is_valid():
            o.name = form.cleaned_data['name']
            o.lastname = form.cleaned_data['lastname']
            o.CI = form.cleaned_data['CI']
            o.destino = form.cleaned_data['destino']
            o.origen = form.cleaned_data['origen']
            o.costo_Pasaje = form.cleaned_data['costo_Pasaje']
            o.fecha = form.cleaned_data['fecha']
            o.save()
            messages.success(request, 'La bonificacion ha sido modificado correctamente', 'alert alert-success alert-lng')
            return redirect('Bonificaciones')
        else:
            messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger alert-lng')
            return redirect('editar-bonificacion', o.id)
    return render(request, 'EditarBonificacion.html', context={ 'o': o })

@login_required(login_url=settings.LOGIN_URL)
def delete_bonificacion(request, pk = None):
    o = Bonificacion.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado la bonificacion a eliminar', 'alert alert-danger alert-lng')
        return redirect('Bonificaciones')
    o = o.first()
    o.delete()
    messages.success(request, 'Se ha eliminado la bonificacion correctamente', 'alert alert-success alert-lng')
    return redirect('Bonificaciones')




@login_required(login_url=settings.LOGIN_URL)
def Dietas(request): 
    dietas = Dieta.objects.all()
    return render(request, "Dieta.html", context = {'dietas': dietas})

@login_required(login_url=settings.LOGIN_URL)
def Crear_Dietas(request):
    if request.method == 'POST': 
        form = DietaForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if len(name) < 2:
                messages.warning(request, 'El nombre debe tener al menos 2 caracteres')
                dietas = Dieta.objects.all()
            if starts_with_uppercase(name) == False:
                messages.warning(request, 'EL nombre no puede empezar con minúsculas')
                dietas = Dieta.objects.all()
           # lastname = form.cleaned_data.get('lastname')
           # if starts_with_uppercase(lastname) == False:
                #messages.warning(request, 'Los apellidos no puede empezar con minúsculas')
                #dietas = Dieta.objects.all()
            
                return render(request, 'Dieta.html', context= {'is_post': True, 'dietas': dietas, 
                    'name_f': request.POST['name'],
                    'lastname_f': request.POST['lastname'],
                    'fechaI_f': request.POST['fechaI'],
                    'fechaF_f': request.POST['fechaF'],
                    'CI_f': request.POST['CI'],
                    'desc_f': request.POST['desc'],
                    
                })
            dieta = {
                'name': form.cleaned_data['name'],
                'lastname': form.cleaned_data['lastname'],
                'fechaI': form.cleaned_data['fechaI'],
                'fechaF': form.cleaned_data['fechaF'],
                'CI': form.cleaned_data['CI'],
                'desc': form.cleaned_data['desc'],
            }
            Dieta.objects.create(**dieta)
            messages.success(request, 'Se ha agregado la dieta correctamente', 'alert alert-success')

            return redirect("Crear-Dieta")    
        else:
            messages.warning(request, 'Formulario inválido.')
            dietas = Dieta.objects.all()
            return render(request, 'Dieta.html', context= {'is_post': True, 'dietas': dietas, 
                'name_f': request.POST['name'],
                'lastname_f': request.POST['lastname'],
                'fechaI_f': request.POST['fechaI'],
                'fechaF_f': request.POST['fechaF'],
                'CI_f': request.POST['CI'],
                'desc_f': request.POST['desc'],
            })
            
      
    return redirect('Dietas')
    

@login_required(login_url=settings.LOGIN_URL)
def editar_dieta(request, pk = None):
    o = Dieta.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado la Dieta a modificar', 'alert alert-danger alert-lng')
        return redirect('Dietas')
    o = o.first()
    if request.method == 'POST':
        form = DietaForm(request.POST)
        if form.is_valid():
            o.name = form.cleaned_data['name']
            o.lastname = form.cleaned_data['lastname']
            o.CI = form.cleaned_data['CI']
            o.fechaI = form.cleaned_data['fechaI']
            o.fechaF = form.cleaned_data['fechaF']
            o.desc = form.cleaned_data['desc']
            o.save()
            messages.success(request, 'La Dieta ha sido modificado correctamente', 'alert alert-success alert-lng')
            return redirect('Dietas')
        else:
            messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger alert-lng')
            return redirect('editar-Dieta', o.id)
    return render(request, 'EditarDieta.html', context={ 'o': o })

@login_required(login_url=settings.LOGIN_URL)
def delete_dieta(request, pk = None):
    o = Dieta.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado la Dieta a eliminar', 'alert alert-danger alert-lng')
        return redirect('Dietas')
    o = o.first()
    o.delete()
    messages.success(request, 'Se ha eliminado la Dieta correctamente', 'alert alert-success alert-lng')
    return redirect('Dietas')


@login_required(login_url=settings.LOGIN_URL)
def Expedientes(request): 
    expedientes = Expediente.objects.all()
    return render(request, "Expedientes.html", context = {'expedientes': expedientes})

@login_required(login_url=settings.LOGIN_URL)
def Crear_Expedientes(request):
    if request.method == 'POST': 
        form = ExpedienteForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if len(name) < 2:
                messages.warning(request, 'El nombre debe tener al menos 2 caracteres')
                expedientes = Expediente.objects.all()
            if starts_with_uppercase(name) == False:
                messages.warning(request, 'EL nombre no puede empezar con minúsculas')
                expedientes = Expediente.objects.all()
            lastname = form.cleaned_data.get('lastname')
            if starts_with_uppercase(lastname) == False:
                messages.warning(request, 'Los apellidos no puede empezar con minúsculas')
                expedientes = Expediente.objects.all()
            
            
                
                return render(request, 'Expedientes.html', context= {'is_post': True, 'expedientes': expedientes, 
                    'name_f': request.POST['name'],
                    'lastname_f': request.POST['lastname'],
                    'fac_f': request.POST['fac'],
                    'dir_f': request.POST['dir'],
                    'CI_f': request.POST['CI'],
                    'prov_f': request.POST['prov'],
                    'mun_f': request.POST['mun'],
                    'sol_f': request.POST['sol'],
                    'fechaC_f': request.POST['fechaC'],
                    'fechaA_f': request.POST['fechaA'],
                })
            expediente = {
                'name': form.cleaned_data['name'],
                'lastname': form.cleaned_data['lastname'],
                'fac': form.cleaned_data['fac'],
                'dir': form.cleaned_data['dir'],
                'CI': form.cleaned_data['CI'],
                'prov': form.cleaned_data['prov'],
                'mun': form.cleaned_data['mun'],
                'sol': form.cleaned_data['sol'],
                'fechaC': form.cleaned_data['fechaC'],
                'fechaA': form.cleaned_data['fechaA'],
            }
            Expediente.objects.create(**expediente)
            messages.success(request, 'Se ha agregado el expediente correctamente', 'alert alert-success')

            return redirect("Crear-Expediente")    
        else:
            messages.warning(request, 'Formulario inválido.')
            expedientes = Expediente.objects.all()
            return render(request, 'Expedientes.html', context= {'is_post': True, 'expedientes': expedientes, 
                'name_f': request.POST['name'],
                'lastname_f': request.POST['lastname'],
                'fac_f': request.POST['fac'],
                'dir_f': request.POST['dir'],
                'CI_f': request.POST['CI'],
                'prov_f': request.POST['prov'],
                'mun_f': request.POST['mun'],
                'sol_f': request.POST['sol'],
                'fechaC_f': request.POST['fechaC'],
                'fechaA_f': request.POST['fechaA'],
            })
            
       # else:
           # print('Hola 3')
           # messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger')
            #bonificaciones = Bonificacion.objects.all()
            #return render(request, 'Bonificaciones.html', context= {'is_post': True, 'bonificaciones': bonificaciones})
    return redirect('Expedientes')
      

@login_required(login_url=settings.LOGIN_URL)
def editar_expediente(request, pk = None):
    o = Expediente.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado el expediente a modificar', 'alert alert-danger alert-lng')
        return redirect('Expedientes')
    o = o.first()
    if request.method == 'POST':
        form = ExpedienteForm(request.POST)
        print('Hola')
        if form.is_valid():
            print('Hola')
            o.name = form.cleaned_data['name']
            o.lastname = form.cleaned_data['lastname']
            o.fac = form.cleaned_data['fac']
            o.dir = form.cleaned_data['dir']
            o.CI = form.cleaned_data['CI']
            o.prov = form.cleaned_data['prov']
            o.mun = form.cleaned_data['mun']
            o.sol = form.cleaned_data['sol']
            o.fechaC = form.cleaned_data['fechaC']
            o.fechaA = form.cleaned_data['fechaA']
            o.save()
            messages.success(request, 'El expediente ha sido modificado correctamente', 'alert alert-success alert-lng')
            return redirect('Expedientes')
        else:
            messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger alert-lng')
            return redirect('editar-expediente', o.id)
    return render(request, 'EditarExpediente.html', context={ 'o': o })

@login_required(login_url=settings.LOGIN_URL)
def delete_expediente(request, pk = None):
    o = Expediente.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado el expediente a eliminar', 'alert alert-danger alert-lng')
        return redirect('Expedientes')
    o = o.first()
    o.delete()
    messages.success(request, 'Se ha eliminado el expediente correctamente', 'alert alert-success alert-lng')
    return redirect('Expedientes')

@login_required(login_url=settings.LOGIN_URL)
def index(request):
    return render(request, "index.html")

@login_required(login_url=settings.LOGIN_URL)
def Inicio(request):
    return render(request, "Inicio.html")

@login_required(login_url=settings.LOGIN_URL)
def Prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "Prestamo.html", context = {'prestamos': prestamos})

@login_required(login_url=settings.LOGIN_URL)
def Crear_Prestamo(request):
    if request.method == 'POST': 
        form = PrestamoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if len(name) < 2:
                messages.warning(request, 'El nombre debe tener al menos 2 caracteres')
                prestamos = Prestamo.objects.all()
            if starts_with_uppercase(name) == False:
                messages.warning(request, 'EL nombre no puede empezar con minúsculas')
                prestamos = Prestamo.objects.all()
            lastname = form.cleaned_data.get('lastname')
            if len(lastname) < 2:
                messages.warning(request, 'El nombre debe tener al menos 2 caracteres')
                prestamos = Prestamo.objects.all()
            if starts_with_uppercase(lastname) == False:
                messages.warning(request, 'EL nombre no puede empezar con minúsculas')
                prestamos = Prestamo.objects.all()
            cant = form.cleaned_data.get('cant')
            if cant <= 0 :
                messages.warning(request, 'El costo del pasaje no puede ser negativo o cero')
                prestamos = Prestamo.objects.all()
                
                return render(request, 'Prestamo.html', context= {'is_post': True, 'prestamos': prestamos, 
                    'name_f': request.POST['name'],
                    'lastname_f': request.POST['lastname'],
                    'fechaI_f': request.POST['fechaI'],
                    'fechaF_f': request.POST['fechaF'],
                    'cant_f': request.POST['cant'],
                    
                })
            prestamo = {
                'name': form.cleaned_data['name'],
                'lastname': form.cleaned_data['lastname'],
                'fechaI': form.cleaned_data['fechaI'],
                'fechaF': form.cleaned_data['fechaF'],
                'cant': form.cleaned_data['cant'],
            }
            Prestamo.objects.create(**prestamo)
            messages.success(request, 'Se ha agregado el prestamo correctamente', 'alert alert-success')

            return redirect("Crear-Prestamo")    
        else:
            messages.warning(request, 'Formulario inválido.')
            prestamos = Prestamo.objects.all()
            return render(request, 'Prestamo.html', context= {'is_post': True, 'prestamos': prestamos, 
                'name_f': request.POST['name'],
                'lastname_f': request.POST['lastname'],
                'fechaI_f': request.POST['fechaI'],
                'fechaF_f': request.POST['fechaF'],
                'cant_f': request.POST['cant'],
            })
            
       # else:
           # print('Hola 3')
           # messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger')
            #bonificaciones = Bonificacion.objects.all()
            #return render(request, 'Bonificaciones.html', context= {'is_post': True, 'bonificaciones': bonificaciones})
    return redirect('Prestamo')


@login_required(login_url=settings.LOGIN_URL)
def editar_prestamo(request, pk = None):
    o = Prestamo.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado el prestamo a modificar', 'alert alert-danger alert-lng')
        return redirect('Prestamo')
    o = o.first()
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            o.name = form.cleaned_data['name']
            o.lastname = form.cleaned_data['lastname']
            o.fechaI = form.cleaned_data['fechaI']
            o.fechaF = form.cleaned_data['fechaF']
            o.cant = form.cleaned_data['cant']
            o.save()
            messages.success(request, 'El prestamo ha sido modificado correctamente', 'alert alert-success alert-lng')
            return redirect('Prestamo')
        else:
            messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger alert-lng')
            return redirect('editar-Prestamo', o.id)
    return render(request, 'EditarPrestamo.html', context={ 'o': o })


@login_required(login_url=settings.LOGIN_URL)
def delete_prestamo(request, pk = None):
    o = Prestamo.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado el prestamo a eliminar', 'alert alert-danger alert-lng')
        return redirect('Prestamo')
    o = o.first()
    o.delete()
    messages.success(request, 'Se ha eliminado el prestamo correctamente', 'alert alert-success alert-lng')
    return redirect('Prestamo')

@login_required(login_url=settings.LOGIN_URL)
def Usuarios(request):
    usuarios = User.objects.all()
    return render(request, "Usuarios.html", context={'usuarios': usuarios})

def Agregar_usuario(request):
    context = {
        'name_form': request.POST.get('name', ''),
        'last_name_form': request.POST.get('last_name', ''),
        'username_form': request.POST.get('username', ''),
        'role_form': request.POST.get('role', ''),
    }
    if request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                name=form.cleaned_data['name'], 
                last_name=form.cleaned_data['last_name'],  
                username=form.cleaned_data['username'], 
                role=form.cleaned_data['role'], 
                password=form.cleaned_data['password'])
            if user is not None:
                messages.success(request, 'Se ha agregado el usuario correctamente', 'alert alert-success alert-lng')
                return redirect('Usuarios')
            else:
                messages.error(request, 'Ha ocurrido un error al crear el usuario', 'alert alert-danger alert-lng')
        else:
            messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger alert-lng')
    usuarios = User.objects.all()
    return render(request, 'Usuarios.html', context=context)

def Editar_usuario(request, pk = None):
    o = User.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado el usuario a modificar', 'alert alert-danger alert-lng')
        return redirect('Usuarios')
    o = o.first()
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=o)
        if form.is_valid():
            o.name = form.cleaned_data['name']
            o.last_name = form.cleaned_data['last_name']
            o.username = form.cleaned_data['username']
            if request.POST.get('password', False):
                o.set_password(request.POST['password'])
            o.role = form.cleaned_data['role']
            o.save()
            messages.success(request, 'Se ha modificado el usuario correctamente', 'alert alert-success alert-lng')
            return redirect('Usuarios')
        else:
            messages.error(request, list(form.errors.as_data().values())[0][0].message, 'alert alert-danger alert-lng')
            return redirect('usuario-editar', o.id)
    return render(request, 'EditarUsuario.html', {'o': o})

def Delete_usuario(request, pk = None):
    o = User.objects.filter(id=pk)
    if not o.exists():
        messages.error(request, 'No se ha encontrado el usuario a eliminar', 'alert alert-danger alert-lng')
        return redirect('Usuarios')
    o = o.first()
    if o.username == 'Administrador':
        messages.error(request, 'No se ha encontrado el usuario a eliminar', 'alert alert-danger alert-lng')
        return redirect('Usuarios')
    o.delete()
    messages.success(request, 'Se ha eliminado el usuario correctamente', 'alert alert-success alert-lng')
    return redirect('Usuarios')





def starts_with_uppercase(s):
    if len(s) > 0:
        return s[0].isupper()
    else:
        return False