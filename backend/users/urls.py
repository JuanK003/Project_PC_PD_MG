from django.urls import path
from .views import UsuarioView

app_name = 'usuarios'

urlpatterns = [
    # Lista de usuarios
    path('usuarios/', UsuarioView.as_view(), name='lista_usuarios'),

    # Detalles de un usuario por ID
    path('usuarios/<str:user_id>/', UsuarioView.as_view(), name='detalle_usuario'),

    # Crear un usuario
    path('usuarios/crear/', UsuarioView.as_view(), name='crear_usuario'),

    # Actualizar un usuario por ID
    path('usuarios/actualizar/<str:user_id>/', UsuarioView.as_view(), name='actualizar_usuario'),

    # Eliminar un usuario por ID
    path('usuarios/eliminar/<str:user_id>/', UsuarioView.as_view(), name='eliminar_usuario'),
]
