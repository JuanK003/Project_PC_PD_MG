from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import pyrebase

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
            "password": data.get("password"),
            "name": data.get("name"),
            "email": data.get("email"),
        }
        
        try:
            # Realizar la operación de creación en Firebase
            user = auth.create_user_with_email_and_password(data.get("email"), data.get("password"))
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

#--------------------------TORNEOS CRUD -----------------------------------------

@method_decorator(csrf_exempt, name='dispatch')
class TorneosView(View):
    def post(self, request):
        data = json.loads(request.body)
        new_torneo = {
                "nombre_torneo": data.get("nombre_torneo"),
                "deporte": data.get("deporte"),
                "fecha_inicio": data.get("fecha_inicio"),
                "fecha_fin": data.get("fecha_fin"),
                "id_usuario": data.get("id_usuario"),
            }

        equipos = data.get("equipos", [])  # Asume que equipos es una lista de objetos equipo

        try:
            # Realizar la operación de creación en Firebase
            torneo_ref = database.child("Torneos").push(new_torneo)
            torneo_id = torneo_ref.key

            # Agregar equipos al torneo
            for equipo in equipos:
                equipo_data = {
                    "nombre": equipo.get("nombre"),
                    "jugadores": equipo.get("jugadores", [])  # Asume que jugadores es una lista de objetos jugador
                }
                equipo_ref = torneo_ref.child("equipos").push(equipo_data)

            return JsonResponse({"message": "Torneo creado exitosamente", "id": torneo_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    def put(self, request, torneo_id):
        data = json.loads(request.body)
        equipo_data = {
            "nombre": data.get("nombre"),
            "jugadores": data.get("jugadores", [])  # Asume que jugadores es una lista de objetos jugador
        }

        try:
            # Agregar el equipo al torneo existente en Firebase
            torneo_ref = database.child("Torneos").child(torneo_id)
            equipo_ref = torneo_ref.child("equipos").push(equipo_data)

            return JsonResponse({"message": "Equipo agregado exitosamente", "equipo_id": equipo_ref.key}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, torneo_id):
        try:
            # Eliminar un torneo de Firebase por su ID
            database.child("Torneos").child(torneo_id).remove()
            return JsonResponse({"message": "Torneo eliminado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, torneo_id, equipo_id):
        data = json.loads(request.body)
        equipo_data = {
            "nombre": data.get("nombre"),
            "jugadores": data.get("jugadores", [])  # Asume que jugadores es una lista de objetos jugador
        }

        try:
            # Actualizar información del equipo en el torneo existente en Firebase
            torneo_ref = database.child("Torneos").child(torneo_id)
            equipo_ref = torneo_ref.child("equipos").child(equipo_id)
            equipo_ref.set(equipo_data)

            return JsonResponse({"message": "Equipo actualizado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, torneo_id, equipo_id):
        try:
            # Eliminar un equipo de un torneo en Firebase por su ID
            torneo_ref = database.child("Torneos").child(torneo_id)
            equipo_ref = torneo_ref.child("equipos").child(equipo_id)
            equipo_ref.remove()

            return JsonResponse({"message": "Equipo eliminado exitosamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

#-----------------------------