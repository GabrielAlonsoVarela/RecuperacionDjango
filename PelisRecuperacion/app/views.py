from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
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

            
            if Usuarios.objects.filter(email=datosFormulario['email']).exists():
                raise ValidationError('El email ya está registrado.')

            
            if Usuarios.objects.filter(nickname=datosFormulario['nickname']).exists():
                raise ValidationError('El nickname ya está registrado.')
            
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

# Vista Log out
@csrf_exempt
def logout(request):
    if request.method != 'PATCH':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        error_response, payload = verify_token(request)
        if error_response:
            return error_response
        usuario_id = payload['id']
    
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token expirado'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Token inválido'}, status=401)

    try:
        usuario = Usuarios.objects.get(pk=usuario_id)
        usuario.token = None
        usuario.save()
        return JsonResponse({'message': 'Sesión cerrada con éxito'}, status=200)
    except Usuarios.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

#Vista info publica
@csrf_exempt
def datos_usuarios(request, id_solicitada):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    try:
        usuario = Usuarios.objects.get(pk = id_solicitada)

        datos_usuario = {
            "avatar": usuario.avatar,
            "nombre": usuario.nombre,
            "apellidos": usuario.apellidos,
            "nickname": usuario.nickname,
            "email": usuario.email,
            "fecha_registro": usuario.fecha.strftime("%Y-%m-%d")
        }

        return JsonResponse(datos_usuario)

    except Usuarios.DoesNotExist:
        return JsonResponse({"error": f"No se encontró el usuario con id: { id_solicitada }"}, status=404)
    

#Vistas Delete usuario
@csrf_exempt
def delete_usuario(request):
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])
    
    try:
        error_response, payload = verify_token(request)
        if error_response:
            return error_response
        
        usuario_id = payload['id']
        usuario = Usuarios.objects.get(pk=usuario_id)
        
        if usuario_id == usuario.pk:
            usuario.delete()
            return JsonResponse({'message': 'Usuario eliminado exitosamente'}, status=200)
        else:
            return JsonResponse({'error': 'No tienes permiso para eliminar al usuario'}, status=403)
    
    except Usuarios.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)



#Vistas Buscar Favorita
@csrf_exempt
def buscar_favoritos(request, id_solicitada):
    if request.method != 'GET':
        return None
    
    usuario = Usuarios.objects.get(pk=id_solicitada)
    lista_favoritos = Favoritas.objects.filter(id_usuario=usuario).select_related('id_pelicula')
    
    respuesta_final = []
    for favorito in lista_favoritos:
        pelicula_actual = favorito.id_pelicula
        diccionario = {
            'id_pelicula': pelicula_actual.id,
            'nombre': pelicula_actual.nombre,
            'imagen': pelicula_actual.imagen,
            'categoria': pelicula_actual.categoria
        }
        respuesta_final.append(diccionario)
    
    return JsonResponse(respuesta_final, safe=False)


#Vistas Post Favorita
@csrf_exempt
def post_favorito(request, id_pelicula):
    if request.method == 'POST':
        try:
            mensaje, payload = verify_token(request)
            print(payload['id'])
            if mensaje:
                return mensaje

            # Verificar si el usuario existe
            try:
                usuario = Usuarios.objects.get(pk=payload['id'])
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

            # Verificar si la película existe
            try:
                pelicula = Peliculas.objects.get(pk=id_pelicula)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Película no encontrada'}, status=404)

            # Crear el nuevo objeto Favoritas
            new_favorito = Favoritas(id_usuario=usuario, id_pelicula=pelicula)
            new_favorito.save()
            return JsonResponse({'message': 'Todo correcto'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Vista Delete favorita     
@csrf_exempt
def delete_favorita(request, id_pelicula): 
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])
    
    try:
        error_response, payload = verify_token(request)
        if error_response:
            return error_response
        
        usuario_id = payload['id']
        usuario = Usuarios.objects.get(pk=usuario_id)
        
        # Buscar la entrada en Favoritas y eliminarla
        try:
            favorita = Favoritas.objects.get(id_usuario=usuario_id, id_pelicula=id_pelicula)
            favorita.delete()
            return JsonResponse({'message': 'Película eliminada de favoritas exitosamente'}, status=200)
        except Favoritas.DoesNotExist:
            return JsonResponse({'error': 'La película no está en la lista de favoritas del usuario'}, status=404)
    
    except Usuarios.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    
    except Usuarios.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

#Vistas agregar Reseña
@csrf_exempt
def agregar_resena(request, id_pelicula):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    try:
        error_response, payload = verify_token(request)
        if error_response:
            return error_response
        
        usuario_id = payload['id']
        usuario = Usuarios.objects.get(pk=usuario_id)
        
        # Obtener el comentario de la solicitud
        data = json.loads(request.body)
        comentario = data.get('comentario', '')
        
        # Crear la reseña
        reseña = Reseñas(
            id_usuario=usuario,
            id_pelicula=Peliculas.objects.get(pk=id_pelicula),
            comentario=comentario
        )
        reseña.save()
        
        return JsonResponse({'message': 'Reseña agregada exitosamente'}, status=200)
    
    except Usuarios.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    except Peliculas.DoesNotExist:
        return JsonResponse({'error': 'Película no encontrada'}, status=404)

#Vistas ver reseñas
@csrf_exempt
def ver_resenas(request, id_pelicula):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    try:
        # Obtener todas las reseñas para la película especificada
        reseñas = Reseñas.objects.filter(id_pelicula=id_pelicula)
        
        # Construir una lista de comentarios
        comentarios = [{'usuario': reseña.id_usuario.nombre, 'comentario': reseña.comentario} for reseña in reseñas]
        
        return JsonResponse(comentarios, safe=False)
    
    except Reseñas.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron reseñas para la película'}, status=404)

#Vistas ver peliculas
@csrf_exempt
def ver_peliculas(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
     
    try:
        search = request.GET.get('search', '')
        limit = int(request.GET.get('limit', 5))
        order = request.GET.get('order', 'nombre')
        page_number = int(request.GET.get('page', 1))

        peliculas = Peliculas.objects.filter(Q(nombre__icontains=search)).order_by(order)
    
        paginator = Paginator(peliculas, limit)
        page = paginator.get_page(page_number)

        peliculas_list = list(page.object_list.values())

        return JsonResponse({
            'peliculas': peliculas_list,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page_number
        })

    except Peliculas.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron películas'}, status=404)

