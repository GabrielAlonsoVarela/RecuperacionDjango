from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
import json, jwt
from .models import Amigos, Peliculas, Vistas, Favoritas, Reseñas, Usuarios
from django.core.paginator import Paginator
import datetime

# Create your views here.

# Configuración de JWT (Json Web Token)
SECRET_KEY = 'Secreto' 

# Función para crear el token JWT
def create_token(id):
    payload = {
        'id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=100),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Función para verificar un token JWT en una solicitud HTTP

@csrf_exempt
def verify_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return JsonResponse({'message': 'Token no encontrado '}, status=401), None
    try:
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        return None, payload
    
    except jwt.ExpiredSignatureError:
        return 'El token ha expirado!', None

# Vista para el registro de nuevos usuarios
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            datosFormulario = json.loads(request.body)

            contraseñaHasheada  = make_password(datosFormulario['contraseña'])
            
            nuevo_usuario = Usuarios(
                nombre=datosFormulario['nombre'],
                apellidos=datosFormulario['apellidos'],
                email=datosFormulario['email'],
                nickname=datosFormulario['nickname'],
                contraseña=contraseñaHasheada, 
                fecha=datetime.datetime.now(), 
            )

            nuevo_usuario.save()

            token = create_token(nuevo_usuario.id)

            nuevo_usuario.token = token

            nuevo_usuario.save()

            return JsonResponse({'message': 'Usuario registrado exitosamente'}, status=201)
        
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=400)
        
# Vista login
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            loguearse = json.loads(request.body)

            usuario = Usuarios.objects.get(nickname=loguearse['nickname'])

            if check_password(loguearse['contraseña'], usuario.contraseña):
                token = create_token(usuario.id)

                return JsonResponse({'token': token}, status=200)
            else:
                return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)
        except Usuarios.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
