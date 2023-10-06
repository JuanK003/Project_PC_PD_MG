from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import pyrebase
import bcrypt

# Configuración de Firebase (asegúrate de que esta configuración sea similar a la que has usado previamente)
firebase_config = {
    "apiKey": "AIzaSyBVMbDxfHz4wtcCZd1tVLsngwOWTNTXltE",
    "authDomain": "pruebadjango-cc7f1.firebaseapp.com",
    "databaseURL": "https://pruebadjango-cc7f1-default-rtdb.firebaseio.com",
    "projectId": "pruebadjango-cc7f1",
    "storageBucket": "pruebadjango-cc7f1.appspot.com",
    "messagingSenderId": "511727626220",
    "appId": "1:511727626220:web:1b2a2a1e849a9f0e03c2c9",
    "measurementId": "G-C003HSYZVR"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
database = firebase.database()

@method_decorator(csrf_exempt, name='dispatch')  # Desactivar protección CSRF para simplificar las pruebas
class UsuarioView(View):
    def post(self, request):
        data = json.loads(request.body)
        new_user = {
            "username": data.get("username"),
            "name": data.get("name"),
            "email": data.get("email"),
        }

        try:
            # Validar y encriptar la contraseña con bcrypt
            password = data.get("password")
            if not password:
                return JsonResponse({"error": "La contraseña es obligatoria"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user["password"] = hashed_password.decode('utf-8')

            # Realizar la operación de creación en Firebase
            database.child("Users").push(new_user)

            return JsonResponse({"message": "Usuario creado exitosamente"}, status=201)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        # Obtener la lista de usuarios desde Firebase
        try:
            users = database.child("Users").get().val()
            if users:
                return JsonResponse(users, status=200, safe=False)
            else:
                return JsonResponse({"error": "No hay usuarios disponibles"}, status=404)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request):
        # Actualizar información de un usuario en Firebase
        data = json.loads(request.body)
        try:
            user_email = data.get("email")
            users = database.child("Users").get().val()
            if user_email in users:
                database.child("Users").child(user_email).update(data)
                return JsonResponse({"message": "Usuario actualizado exitosamente"}, status=200)
            else:
                return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request):
        # Eliminar un usuario de Firebase por correo electrónico
        data = json.loads(request.body)
        try:
            user_email = data.get("email")
            users = database.child("Users").get().val()
            if user_email in users:
                database.child("Users").child(user_email).remove()
                return JsonResponse({"message": "Usuario eliminado exitosamente"}, status=200)
            else:
                return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class TournamentView(View):
    def post(self, request):
        data = json.loads(request.body)
        new_tournament = {
            "name_tournament": data.get("name_tournament"),
            "sport": data.get("sport"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "id_user": data.get("id_user"),
        }

        teams = data.get("teams", [])  # Asume que teams es una lista de objetos equipo

        try:
            # Realizar la operación de creación en Firebase
            tournament_ref = database.child("Tournaments").push(new_tournament)
            tournament_id = tournament_ref.key

            # Agregar Teams al torneo
            for team in teams:
                team_data = {
                    "name": team.get("name"),
                    "players": team.get("players", [])  # Asume que players es una lista de objetos jugador
                }
                tournament_ref.child("Teams").push(team_data)

            return JsonResponse({"message": "Torneo creado exitosamente", "id": tournament_id}, status=201)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, torneo_id=None):
        if torneo_id:
            try:
                # Obtener información de un torneo específico en Firebase
                torneo_data = database.child("Tournaments").child(torneo_id).get().val()
                if torneo_data:
                    return JsonResponse(torneo_data, status=200)
                else:
                    return JsonResponse({"error": "El torneo no existe"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                # Obtener la lista de torneos desde Firebase
                torneos = database.child("Tournaments").get().val()
                if torneos:
                    return JsonResponse(torneos, status=200)
                else:
                    return JsonResponse({"error": "No hay torneos disponibles"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, torneo_id, equipo_id=None):
        data = json.loads(request.body)
        equipo_data = {
            "name": data.get("name"),
            "players": data.get("players", [])  # Asume que players es una lista de objetos jugador
        }

        try:
            if equipo_id:
                # Actualizar información del equipo en el torneo existente en Firebase
                torneo_ref = database.child("Tournaments").child(torneo_id).child("Teams").child(equipo_id)
                torneo_ref.update(equipo_data)
                return JsonResponse({"message": "Equipo actualizado exitosamente"}, status=200)
            else:
                # Agregar el equipo al torneo existente en Firebase
                torneo_ref = database.child("Tournaments").child(torneo_id).child("Teams").push(equipo_data)
                equipo_id = torneo_ref.key
                return JsonResponse({"message": "Equipo agregado exitosamente", "equipo_id": equipo_id}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, torneo_id, equipo_id):
        try:
            # Eliminar un equipo de un torneo en Firebase por su ID
            torneo_ref = database.child("Tournaments").child(torneo_id).child("Teams").child(equipo_id)
            torneo_ref.remove()
            return JsonResponse({"message": "Equipo eliminado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class TeamsView(View):
    def post(self, request):
        # Crear un nuevo equipo y sus jugadores en Firebase
        data = json.loads(request.body)
        name = data.get("name")
        players = data.get("players", [])

        try:
            # Crear el equipo en Firebase
            equipo_ref = database.child("Teams").push({"name": name})

            # Crear los jugadores del equipo en Firebase
            for jugador_data in players:
                jugador_ref = equipo_ref.child("players").push(jugador_data)

            return JsonResponse({"message": "Equipo creado exitosamente"}, status=201)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        # Obtener la lista de equipos y sus jugadores desde Firebase
        try:
            teams = database.child("Teams").get().val()
            if teams:
                return JsonResponse(teams, status=200, safe=False)
            else:
                return JsonResponse({"error": "No hay equipos disponibles"}, status=404)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request):
        # Actualizar información de un equipo y sus jugadores en Firebase
        data = json.loads(request.body)
        team_id = data.get("team_id")
        name = data.get("name")
        players = data.get("players", [])

        try:
            equipo_ref = database.child("Teams").child(team_id)
            equipo_ref.update({"name": name})

            # Eliminar los jugadores existentes del equipo en Firebase
            equipo_ref.child("players").delete()

            # Crear los jugadores actualizados en Firebase
            for jugador_data in players:
                jugador_ref = equipo_ref.child("players").push(jugador_data)

            return JsonResponse({"message": "Equipo actualizado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request):
        # Eliminar un equipo y sus jugadores de Firebase
        data = json.loads(request.body)
        team_id = data.get("team_id")

        try:
            equipo_ref = database.child("Teams").child(team_id)
            equipo_ref.delete()
            return JsonResponse({"message": "Equipo eliminado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PlayoffsView(View):
    def get(self, request, playoff_id=None):
        if playoff_id:
            try:
                # Obtener información de un playoff específico en Firebase
                playoff_data = database.child("Playoffs").child(playoff_id).get().val()
                if playoff_data:
                    return JsonResponse(playoff_data, status=200)
                else:
                    return JsonResponse({"error": "El playoff no existe"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                # Obtener la lista de playoffs desde Firebase
                playoffs = database.child("Playoffs").get().val()
                if playoffs:
                    return JsonResponse(playoffs, status=200)
                else:
                    return JsonResponse({"error": "No hay playoffs disponibles"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)

    def post(self, request):
        data = json.loads(request.body)
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        phases = data.get('phases', [])

        try:
            # Crear un nuevo playoff en Firebase
            new_playoff = {
                "start_date": start_date,
                "end_date": end_date,
                "phases": phases
            }
            playoff_ref = database.child("Playoffs").push(new_playoff)
            playoff_id = playoff_ref.key

            return JsonResponse({"message": "Playoff creado exitosamente", "id": playoff_id}, status=201)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, playoff_id):
        data = json.loads(request.body)
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        phases = data.get('phases', [])

        try:
            # Actualizar información de un playoff en Firebase
            playoff_data = {
                "start_date": start_date,
                "end_date": end_date,
                "phases": phases
            }
            database.child("Playoffs").child(playoff_id).update(playoff_data)

            return JsonResponse({"message": "Playoff actualizado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, playoff_id):
        try:
            # Eliminar un playoff de Firebase por su ID
            database.child("Playoffs").child(playoff_id).remove()
            return JsonResponse({"message": "Playoff eliminado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class PlayersView(View):
    def post(self, request):
        data = json.loads(request.body)
        player_data = {
            "player_name": data.get("player_name"),
            "identifier_number": data.get("identifier_number"),
            "position": data.get("position"),
            "number": data.get("number"),
        }

        try:
            # Realizar la operación de creación en Firebase
            player_ref = database.child("Players").push(player_data)
            player_id = player_ref.key

            return JsonResponse({"message": "Jugador creado exitosamente", "id": player_id}, status=201)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, player_id=None):
        if player_id:
            try:
                # Obtener información de un jugador específico en Firebase
                player_data = database.child("Players").child(player_id).get().val()
                if player_data:
                    return JsonResponse(player_data, status=200)
                else:
                    return JsonResponse({"error": "El jugador no existe"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                # Obtener la lista de jugadores desde Firebase
                players = database.child("Players").get().val()
                if players:
                    return JsonResponse(players, status=200)
                else:
                    return JsonResponse({"error": "No hay jugadores disponibles"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, player_id):
        data = json.loads(request.body)
        player_data = {
            "player_name": data.get("player_name"),
            "identifier_number": data.get("identifier_number"),
            "position": data.get("position"),
            "number": data.get("number"),
        }

        try:
            # Actualizar información de un jugador en Firebase
            database.child("Players").child(player_id).update(player_data)
            return JsonResponse({"message": "Jugador actualizado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, player_id):
        try:
            # Eliminar un jugador de Firebase por su ID
            database.child("Players").child(player_id).remove()
            return JsonResponse({"message": "Jugador eliminado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PhasesView(View):
    def post(self, request):
        data = json.loads(request.body)
        phase_data = {
            "phase_name": data.get("phase_name"),
            # Otros campos relevantes para la fase
        }

        try:
            # Realizar la operación de creación en Firebase
            phase_ref = database.child("Phases").push(phase_data)
            phase_id = phase_ref.key

            return JsonResponse({"message": "Fase creada exitosamente", "id": phase_id}, status=201)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, phase_id=None):
        if phase_id:
            try:
                # Obtener información de una fase específica en Firebase
                phase_data = database.child("Phases").child(phase_id).get().val()
                if phase_data:
                    return JsonResponse(phase_data, status=200)
                else:
                    return JsonResponse({"error": "La fase no existe"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                # Obtener la lista de fases desde Firebase
                phases = database.child("Phases").get().val()
                if phases:
                    return JsonResponse(phases, status=200)
                else:
                    return JsonResponse({"error": "No hay fases disponibles"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, phase_id):
        data = json.loads(request.body)
        phase_data = {
            "phase_name": data.get("phase_name"),
            # Actualizar otros campos relevantes para la fase
        }

        try:
            # Actualizar información de una fase en Firebase
            database.child("Phases").child(phase_id).update(phase_data)
            return JsonResponse({"message": "Fase actualizada exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, phase_id):
        try:
            # Eliminar una fase de Firebase por su ID
            database.child("Phases").child(phase_id).remove()
            return JsonResponse({"message": "Fase eliminada exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class MatchesView(View):
    def post(self, request):
        data = json.loads(request.body)
        match_data = {
            "team_1": data.get("team_1"),
            "team_2": data.get("team_2"),
            "result": data.get("result"),
            # Otros campos relevantes para el partido
        }

        try:
            # Realizar la operación de creación en Firebase
            match_ref = database.child("Matches").push(match_data)
            match_id = match_ref.key

            return JsonResponse({"message": "Partido creado exitosamente", "id": match_id}, status=201)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, match_id=None):
        if match_id:
            try:
                # Obtener información de un partido específico en Firebase
                match_data = database.child("Matches").child(match_id).get().val()
                if match_data:
                    return JsonResponse(match_data, status=200)
                else:
                    return JsonResponse({"error": "El partido no existe"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                # Obtener la lista de partidos desde Firebase
                matches = database.child("Matches").get().val()
                if matches:
                    return JsonResponse(matches, status=200)
                else:
                    return JsonResponse({"error": "No hay partidos disponibles"}, status=404)
            except pyrebase.exceptions.RequestAborted as e:
                return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, match_id):
        data = json.loads(request.body)
        match_data = {
            "team_1": data.get("team_1"),
            "team_2": data.get("team_2"),
            "result": data.get("result"),
            # Actualizar otros campos relevantes para el partido
        }

        try:
            # Actualizar información de un partido en Firebase
            database.child("Matches").child(match_id).update(match_data)
            return JsonResponse({"message": "Partido actualizado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, match_id):
        try:
            # Eliminar un partido de Firebase por su ID
            database.child("Matches").child(match_id).remove()
            return JsonResponse({"message": "Partido eliminado exitosamente"}, status=200)
        except pyrebase.exceptions.RequestAborted as e:
            return JsonResponse({"error": str(e)}, status=400)
