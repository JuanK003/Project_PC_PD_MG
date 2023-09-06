from django.urls import path
from .views import UsuarioView, TorneosView

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

    # Ruta para crear un nuevo torneo y agregar equipos
    path('torneos/', TorneosView.as_view(), name='crear_torneo'),

    # Ruta para obtener una lista de todos los torneos
    path('torneos/', TorneosView.as_view(), name='lista_torneos'),

    # Ruta para obtener, actualizar o eliminar un torneo específico
    path('torneos/<str:torneo_id>/', TorneosView.as_view(), name='torneo_detail'),

    # Ruta para agregar un equipo a un torneo específico
    path('torneos/<str:torneo_id>/equipos/', TorneosView.as_view(), name='agregar_equipo'),

    # Ruta para actualizar o eliminar un equipo en un torneo específico
    path('torneos/<str:torneo_id>/equipos/<str:equipo_id>/', TorneosView.as_view(), name='equipo_detail'),
]
