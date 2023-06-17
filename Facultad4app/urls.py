from django.urls import path
from Facultad4app import views
from .views import index




urlpatterns = [
    # path('', index, name='index'),
    path('', views.Inicio, name="index" ),
    path('login', views.auth_login, name="login" ),
    path('logout', views.auth_logout, name="logout" ),
  #  path('register/', views.register, name="register" ),
    path('Bonificaciones', views.Bonificaciones, name="Bonificaciones"),
    path('Crear-Bonificacion', views.Crear_Bonificaciones, name="Crear-Bonificacion"),
    path('Editar-Bonificaciones/<int:pk>', views.editar_bonificacion, name="editar-bonificacion"),
    path('delete-bonificacion/<int:pk>', views.delete_bonificacion, name="delete-bonificacion"),
   # path('buscar_bonificaciones/<int:pk>', views.buscar_bonificaciones, name="buscar_bonificaciones"),
    path('Dietas', views.Dietas, name="Dietas"),
    path('Crear-Dieta', views.Crear_Dietas, name="Crear-Dieta"),
    path('Editar-Dietas/<int:pk>', views.editar_dieta, name="editar-Dieta"),
    path('delete-dieta/<int:pk>', views.delete_dieta, name="delete-Dieta"),
    path('Expedientes', views.Expedientes, name="Expedientes"),
    path('Crear-Expediente', views.Crear_Expedientes, name="Crear-Expediente"),
    path('editar-expediente/<int:pk>', views.editar_expediente, name="editar-expediente"),
    path('delete-expediente/<int:pk>', views.delete_expediente, name="delete-expediente"),
    path('Inicio', views.Inicio, name="Inicio"),
    path('Prestamo', views.Prestamos, name="Prestamo"),
    path('Crear-Prestamo', views.Crear_Prestamo, name="Crear-Prestamo"),
    path('Editar-Prestamo/<int:pk>', views.editar_prestamo, name="editar-Prestamo"),
    path('delete-Prestamo/<int:pk>', views.delete_prestamo, name="delete-Prestamo"),
    path('Usuarios', views.Usuarios, name="Usuarios"),
    path('Usuarios/editar/<int:pk>', views.Editar_usuario, name="usuario-editar"),
    path('Usuarios/eliminar/<int:pk>', views.Delete_usuario, name="usuario-eliminar"),
    path('Usuarios/agregar', views.Agregar_usuario, name="usuario-agregar"),
       
]