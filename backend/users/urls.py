from django.urls import path
from .views import UsuarioView, TournamentView, TeamsView, PlayoffsView, PlayersView, PhasesView, MatchesView

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

#-------------------------------------------------------------------------------------------------------
    
    # Ruta para crear un nuevo torneo y agregar equipos
    path('torneos/', TournamentView.as_view(), name='crear_torneo'),

    # Ruta para obtener una lista de todos los torneos o crear uno nuevo
    path('torneos/lista/', TournamentView.as_view(), name='lista_torneos'),

    # Ruta para obtener, actualizar o eliminar un torneo específico
    path('torneos/<str:torneo_id>/', TournamentView.as_view(), name='torneo_detail'),

    # Ruta para agregar un equipo a un torneo específico
    path('torneos/<str:torneo_id>/equipos/', TournamentView.as_view(), name='agregar_equipo'),

    # Ruta para actualizar o eliminar un equipo en un torneo específico
    path('torneos/<str:torneo_id>/equipos/<str:equipo_id>/', TournamentView.as_view(), name='equipo_detail'),
    
    #-------------------------------------------------------------------------------------------------------
    
    # Lista de equipos
    path('equipos/', TeamsView.as_view(), name='lista_equipos'),

    # Detalles de un equipo por ID
    path('equipos/<str:equipo_id>/', TeamsView.as_view(), name='detalle_equipo'),

    # Crear un equipo
    path('equipos/crear/', TeamsView.as_view(), name='crear_equipo'),

    # Actualizar un equipo por ID
    path('equipos/actualizar/<str:equipo_id>/', TeamsView.as_view(), name='actualizar_equipo'),

    # Eliminar un equipo por ID
    path('equipos/eliminar/<str:equipo_id>/', TeamsView.as_view(), name='eliminar_equipo'),
    
    #-------------------------------------------------------------------------------------------------------
    
    # Lista de playoffs
    path('playoffs/', PlayoffsView.as_view(), name='lista_playoffs'),

    # Detalles de un playoff por ID
    path('playoffs/<str:playoff_id>/', PlayoffsView.as_view(), name='detalle_playoff'),

    # Crear un playoff
    path('playoffs/crear/', PlayoffsView.as_view(), name='crear_playoff'),

    # Actualizar un playoff por ID
    path('playoffs/actualizar/<str:playoff_id>/', PlayoffsView.as_view(), name='actualizar_playoff'),

    # Eliminar un playoff por ID
    path('playoffs/eliminar/<str:playoff_id>/', PlayoffsView.as_view(), name='eliminar_playoff'), 

#-------------------------------------------------------------------------------------------------------    
        # Rutas para las entidades Players (jugadores)
    path('jugadores/', PlayersView.as_view(), name='lista_jugadores'),
    path('jugadores/crear/', PlayersView.as_view(), name='crear_jugador'),
    path('jugadores/<str:player_id>/', PlayersView.as_view(), name='detalle_jugador'),
    path('jugadores/actualizar/<str:player_id>/', PlayersView.as_view(), name='actualizar_jugador'),
    path('jugadores/eliminar/<str:player_id>/', PlayersView.as_view(), name='eliminar_jugador'),
    
#-------------------------------------------------------------------------------------------------------
  
    # Rutas para las entidades Phases (fases)
    path('fases/', PhasesView.as_view(), name='lista_fases'),
    path('fases/crear/', PhasesView.as_view(), name='crear_fase'),
    path('fases/<str:phase_id>/', PhasesView.as_view(), name='detalle_fase'),
    path('fases/actualizar/<str:phase_id>/', PhasesView.as_view(), name='actualizar_fase'),
    path('fases/eliminar/<str:phase_id>/', PhasesView.as_view(), name='eliminar_fase'),
    
#-------------------------------------------------------------------------------------------------------

    # Rutas para las entidades Matches (partidos)
    path('partidos/', MatchesView.as_view(), name='lista_partidos'),
    path('partidos/crear/', MatchesView.as_view(), name='crear_partido'),
    path('partidos/<str:match_id>/', MatchesView.as_view(), name='detalle_partido'),
    path('partidos/actualizar/<str:match_id>/', MatchesView.as_view(), name='actualizar_partido'),
    path('partidos/eliminar/<str:match_id>/', MatchesView.as_view(), name='eliminar_partido'),
]
