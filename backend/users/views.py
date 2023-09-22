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
        # Crear un nuevo usuario en Firebase
        data = json.loads(request.body)
        new_user = {
            "username": data.get("username"),
            "name": data.get("name"),
            "email": data.get("email"),
        }

        try:
            # Encripta contraseña bcrypt
            password = data.get("password").encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            print("Contraseña encriptada:", hashed_password)
            # Realizar la operación de creación en Firebase con la contraseña encriptada
            user = auth.create_user_with_email_and_password(data.get("email"), hashed_password.decode('utf-8'))
            database.child("Users").push(new_user)  # Utiliza push para generar automáticamente una clave única
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
            torneo_id = torneo_ref.key

            # Agregar Teams al torneo
            for equipo in Teams:
                equipo_data = {
                    "name": equipo.get("name"),
                    "players": equipo.get("players", [])  # Asume que players es una lista de objetos jugador
                }
                equipo_ref = torneo_ref.child("Teams").push(equipo_data)

            return JsonResponse({"message": "Torneo creado exitosamente", "id": torneo_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    def put(self, request, torneo_id):
        data = json.loads(request.body)
        equipo_data = {
            "name": data.get("name"),
            "players": data.get("players", [])  # Asume que players es una lista de objetos jugador
        }

        try:
            # Agregar el equipo al torneo existente en Firebase
            torneo_ref = database.child("Tournament").child(torneo_id)
            equipo_ref = torneo_ref.child("Teams").push(equipo_data)

            return JsonResponse({"message": "Equipo agregado exitosamente", "equipo_id": equipo_ref.key}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, torneo_id):
        try:
            # Eliminar un torneo de Firebase por su ID
            database.child("Tournament").child(torneo_id).remove()
            return JsonResponse({"message": "Torneo eliminado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, torneo_id, equipo_id):
        data = json.loads(request.body)
        equipo_data = {
            "name": data.get("name"),
            "players": data.get("players", [])  # Asume que players es una lista de objetos jugador
        }

        try:
            # Actualizar información del equipo en el torneo existente en Firebase
            torneo_ref = database.child("Tournament").child(torneo_id)
            equipo_ref = torneo_ref.child("Teams").child(equipo_id)
            equipo_ref.set(equipo_data)

            return JsonResponse({"message": "Equipo actualizado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, torneo_id, equipo_id):
        try:
            # Eliminar un equipo de un torneo en Firebase por su ID
            torneo_ref = database.child("Tournament").child(torneo_id)
            equipo_ref = torneo_ref.child("Teams").child(equipo_id)
            equipo_ref.remove()

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