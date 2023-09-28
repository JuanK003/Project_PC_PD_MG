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
            # Encripta la contraseña con bcrypt
            password = data.get("password").encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            print("Contraseña encriptada:", hashed_password)

            # Almacena la contraseña encriptada en el diccionario
            new_user["password"] = hashed_password.decode('utf-8')

            # Realiza la operación de creación en Firebase sin la contraseña encriptada
            database.child("Users").push(new_user)

            return JsonResponse({"message": "Usuario creado exitosamente"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        # Obtener la lista de usuarios desde Firebase
        try:
            users = database.child("Users").get().val()
            if users:
                return JsonResponse(users, status=200, safe=False)
            else:
                return JsonResponse({"error": "No hay usuarios disponibles"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request):
        # Actualizar información de un usuario en Firebase
        data = json.loads(request.body)
        try:
            # Asume que el usuario a actualizar está identificado por su correo electrónico
            user_email = data.get("email")
            users = database.child("Users").get().val()
            if user_email in users:
                database.child("Users").child(user_email).update(data)
                return JsonResponse({"message": "Usuario actualizado exitosamente"}, status=200)
            else:
                return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        except Exception as e:
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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

#--------------------------Tournament CRUD -----------------------------------------

@method_decorator(csrf_exempt, name='dispatch')
class TournamentView(View):
    def post(self, request):
        data = json.loads(request.body)
        new_torneo = {
            "name_tournament": data.get("name_tournament"),
            "sport": data.get("sport"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "id_user": data.get("id_user"),
        }

        Teams = data.get("Teams", [])  # Asume que Teams es una lista de objetos equipo

        try:
            # Realizar la operación de creación en Firebase
            torneo_ref = database.child("Tournament").push(new_torneo)
            torneo_id = torneo_ref['name']  # Obtener la clave generada automáticamente

            # Agregar Teams al torneo
            for equipo in Teams:
                equipo_data = {
                    "name": equipo.get("name"),
                    "players": equipo.get("players", [])  # Asume que players es una lista de objetos jugador
                }
                torneo_ref.child("Teams").push(equipo_data)

            return JsonResponse({"message": "Torneo creado exitosamente", "id": torneo_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, torneo_id=None):
        if torneo_id:
            try:
                # Obtener información de un torneo específico en Firebase
                torneo_data = database.child("Tournament").child(torneo_id).get().val()
                if torneo_data:
                    return JsonResponse(torneo_data, status=200)
                else:
                    return JsonResponse({"error": "El torneo no existe"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                # Obtener la lista de torneos desde Firebase
                torneos = database.child("Tournament").get().val()
                if torneos:
                    return JsonResponse(torneos, status=200)
                else:
                    return JsonResponse({"error": "No hay torneos disponibles"}, status=404)
            except Exception as e:
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
                torneo_ref = database.child("Tournament").child(torneo_id).child("Teams").child(equipo_id)
                torneo_ref.set(equipo_data)
                return JsonResponse({"message": "Equipo actualizado exitosamente"}, status=200)
            else:
                # Agregar el equipo al torneo existente en Firebase
                torneo_ref = database.child("Tournament").child(torneo_id).child("Teams").push(equipo_data)
                equipo_id = torneo_ref.key
                return JsonResponse({"message": "Equipo agregado exitosamente", "equipo_id": equipo_id}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, torneo_id, equipo_id):
        try:
            # Eliminar un equipo de un torneo en Firebase por su ID
            torneo_ref = database.child("Tournament").child(torneo_id).child("Teams").child(equipo_id)
            torneo_ref.remove()
            return JsonResponse({"message": "Equipo eliminado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

#----------------------------- Teams CRUD ---------------------------------------

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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        # Obtener la lista de equipos y sus jugadores desde Firebase
        try:
            teams = database.child("Temas").get().val()
            if teams:
                return JsonResponse(teams, status=200, safe=False)
            else:
                return JsonResponse({"error": "No hay equipos disponibles"}, status=404)
        except Exception as e:
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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request):
        # Eliminar un equipo y sus jugadores de Firebase
        data = json.loads(request.body)
        team_id = data.get("team_id")

        try:
            equipo_ref = database.child("Teams").child(team_id)
            equipo_ref.delete()
            return JsonResponse({"message": "Equipo eliminado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
#----------------------------- PlayOffs CRUD ---------------------------------------

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
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            try:
                # Obtener la lista de playoffs desde Firebase
                playoffs = database.child("Playoffs").get().val()
                if playoffs:
                    return JsonResponse(playoffs, status=200)
                else:
                    return JsonResponse({"error": "No hay playoffs disponibles"}, status=404)
            except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, playoff_id):
        try:
            # Eliminar un playoff de Firebase por su ID
            database.child("Playoffs").child(playoff_id).remove()
            return JsonResponse({"message": "Playoff eliminado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)