"""
URL configuration for PelisRecuperacion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('sesion/', views.logout),
    path('users/<int:id_solicitada>', views.datos_usuarios),
    path('user/', views.delete_usuario),
    path('users/<int:id_solicitada>/favoritos/', views.buscar_favoritos),
    path('pelicula/<int:id_pelicula>/favorita',views.post_favorito),
    path('pelicula/<int:id_pelicula>/delfavorita',views.delete_favorita),
    path('pelicula/<int:id_pelicula>/postresenas',views.agregar_resena),
    path('pelicula/<int:id_pelicula>/resenas',views.ver_resenas),
    path('peliculas/', views.ver_peliculas)
]  