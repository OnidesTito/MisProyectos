from django import forms
from .models import Bonificacion, Dieta, Expediente, Prestamo, User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.core import validators

class UserAddForm(forms.ModelForm):
    
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['name', 'last_name', 'username', 'password', 'role']
        error_messages = {
            'name': {
                'required': 'El nombre es requerido'
            },
            'last_name': {
                'required': 'Los apellidos son requeridos'
            },
            'username': {
                'required': 'El usuario es requerido',
                'unique': 'El usuario ya existe en la base de datos'
            },
            'password': {
                'required': 'La contraseña es requerida',
            },
            'role': {
                'required': 'El rol es requerido'
            }
        }
        
class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['name', 'last_name', 'username', 'role']
        error_messages = {
            'name': {
                'required': 'El nombre es requerido'
            },
            'last_name': {
                'required': 'Los apellidos son requeridos'
            },
            'username': {
                'required': 'El usuario es requerido',
                'unique': 'El usuario ya existe en la base de datos'
            },
            'role': {
                'required': 'El rol es requerido'
            }
        }
        
    def clean_username(self):
        username = self.cleaned_data['username']
        user_id = self.instance.id  # Obtiene el ID del usuario que se está actualizando

        # Comprueba si el nombre de usuario ya existe para otro usuario en la base de datos
        if User.objects.exclude(id=user_id).filter(username=username).exists():
            raise ValidationError('El nombre de usuario ya está en uso.')

        return username

class BonificacionForm(forms.ModelForm):
    
    class Meta:
        model = Bonificacion
        fields = ['name', 'lastname', 'CI', 'destino', 'origen', 'costo_Pasaje', 'fecha']
        name = forms.CharField(label='name', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        lastname = forms.CharField(label='lastname', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        origen = forms.CharField(label='origen', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        destino = forms.CharField(label='destino', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        error_messages = {
            'name': {
                'required': 'El nombre es requerido'
            },
            'lastname': {
                'required': 'Los apellidos son requeridos'
            },
            'CI': {
                'required': 'El carnet de identidad es requerido'
            },
            'destino': {
                'required': 'El destino es requerido'
            },
            'origen': {
                'required': 'El origen es requerido'
            },
            'costo_Pasaje': {
                'required': 'El costo del pasaje es requerido'
            },
            'fecha': {
                'required': 'La fecha es requerida'
            },
        }

class DietaForm(forms.ModelForm):

    class Meta:
        model = Dieta
        fields = ['name', 'lastname', 'fechaI','fechaF','CI','desc']
        name = forms.CharField(label='name', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        lastname = forms.CharField(label='lastname', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        error_messages = {
            'name': {
                'required': 'El nombre es requerido'
            },
            'lastname': {
                'required': 'Los apellidos son requeridos'
            },
            'CI': {
                'required': 'El carnet de identidad es requerido'
            },
            
            'fechaI': {
                'required': 'La fecha de inicio es requerida'
            },

            'fechaF': {
                'required': 'La fecha de fin es requerida'
            },
            
            'desc': {
                'required': 'La descripcion es requerida'
            },
        }

class ExpedienteForm(forms.ModelForm):

    class Meta:
        model = Expediente
        fields = ['name', 'lastname', 'fac', 'dir', 'CI', 'prov', 'mun', 'sol', 'fechaC', 'fechaA']
        error_messages = {
            'name': {
                'required': 'El nombre es requerido'
            },
            'lastname': {
                'required': 'Los apellidos son requeridos'
            },
            'fac': {
                'required': 'La facultad es requerido'
            },
            'dir': {
                'required': 'La direccion es requerido'
            },
            'CI': {
                'required': 'El carnet de identidad es requerido'
            },
            'prov': {
                'required': 'La provincia es requerida'
            },
            'mun': {
                'required': 'El municipio es requerido'
            },
            'sol': {
                'required': 'El solapin es requerido'
            },
            'fechaC': {
                'required': 'La fecha de creacion es requerida'
            },
            'fechaA': {
                'required': 'La fecha de aprobacion es requerida'
            },
        }   

class PrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo
        fields = ['name', 'lastname', 'fechaI','fechaF','cant']
        name = forms.CharField(label='name', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        lastname = forms.CharField(label='lastname', validators=[validators.RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$', 'Por favor, introduce solo letras.')])
        error_messages = {
            'name': {
                'required': 'El nombre es requerido'
            },
            'lastname': {
                'required': 'Los apellidos son requeridos'
            },
           
            'fechaI': {
                'required': 'La fecha de inicio es requerida'
            },

            'fechaF': {
                'required': 'La fecha de fin es requerida'
            },
             'cant': {
                'required': 'La cantidad del prestamo es requerida'
            },
            
              
        }     