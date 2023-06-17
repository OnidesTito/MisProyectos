from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validate_length(value):
    valid = True
    for v in value:
        try:
            int(v)
        except Exception:
            valid = False
    if(valid):
        if len(value) != 11:
            raise ValidationError(
                ('%(value)s El CI debe contener 11 dígitos. Y no puede contener letras'),
                params={"value": value},
            )
    else:
        raise ValidationError(
            ('%(value)s El CI debe contener 11 dígitos. Y no puede contener letras'),
            params={"value": value},
        )

class ManagerUser(BaseUserManager):

    def create_user(self, username, name, last_name, role, password=None):
        if not username:
            raise ValueError('El usuario debe tener un usuario válido')
        user = self.model(
            username=username,
            name=name,
            last_name=last_name,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user_with_role(self, username, name, last_name, password, role):
        user = self.create_user(username, name, last_name, password)
        user.set_password(password)
        if not Group.objects.all().filter(name=role).exists():
            Group.objects.create(name=role)
        group = Group.objects.get(name=role)
        user.groups.add(group)
        user.save(self._db)
        return user


    def create_staff_user(self, username, name, last_name, password):
        user = self.create_user(username, name, last_name, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, last_name, password):
        user = self.create_user(username, name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=80, verbose_name="Nombre")
    last_name = models.CharField(max_length=80, verbose_name="Apellidos")
    username = models.CharField(max_length=80, verbose_name="Usuario", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    role = models.CharField(max_length=80, verbose_name='Rol', default='Administrador')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ManagerUser()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'last_name']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_full_name(self):
        return self.name + ' ' + self.last_name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# Create your models here.
class Bonificacion(models.Model):
    name= models.CharField(max_length=50, verbose_name="Nombre", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    lastname= models.CharField(max_length=50, verbose_name="Apellidos", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    CI=models.CharField(max_length=11, verbose_name="CI", null=False, validators=[validate_length])
    destino= models.CharField(max_length=50, verbose_name="Destino", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    origen= models.CharField(max_length=50, verbose_name="Origen", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    costo_Pasaje=models.IntegerField(verbose_name="costo pasaje", null=False)
    fecha=models.DateField(verbose_name="Fecha")

class Dieta(models.Model):
    name= models.CharField(max_length=50, verbose_name="Nombre", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    lastname= models.CharField(max_length=50, verbose_name="Apellidos", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    fechaI=models.DateField(verbose_name="Fecha Inicio de la dieta")  
    fechaF=models.DateField(verbose_name="Fecha Fin de la dieta")  
    CI=models.CharField(max_length=11, verbose_name="CI", null=False, validators=[validate_length])
    desc=models.TextField(verbose_name="Descripcion")  

class Expediente(models.Model):
    name= models.CharField(max_length=50, verbose_name="Nombre")
    lastname= models.CharField(max_length=50, verbose_name="Apellidos")
    fac=models.CharField(verbose_name="Facultad", null=False)
    dir=models.CharField(verbose_name="Direccion", null=False)
    CI=models.CharField(verbose_name="CI", null=False)
    prov=models.CharField(verbose_name="Provincia", null=False)
    mun=models.CharField(verbose_name="Municipio", null=False)
    sol=models.CharField(verbose_name="Solapin", null=False)
    fechaC=models.DateField(verbose_name="Fecha Inicio de creacion")  
    fechaA=models.DateField(verbose_name="Fecha Fin de aprobacion")  
    
class Prestamo(models.Model):
    name= models.CharField(max_length=50, verbose_name="Nombre", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    lastname= models.CharField(max_length=50, verbose_name="Apellidos", validators=[RegexValidator(r'^[a-zA-ZñáéíóúüÑÁÉÍÓÚÜ_\s]+$')])
    fechaI=models.DateField(verbose_name="Fecha Inicio del Prestamo")  
    fechaF=models.DateField(verbose_name="Fecha Fin del Prestamo")  
    cant=models.IntegerField(verbose_name="cant", null=False)
    
    