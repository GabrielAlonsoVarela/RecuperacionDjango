# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Amigos(models.Model):
    id_usuario = models.OneToOneField('Usuarios', models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_amigo = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_amigo', related_name='amigos_amigo')

    class Meta:
        managed = False
        db_table = 'Amigos'
        unique_together = (('id_usuario', 'id_amigo'),)


class Favoritas(models.Model):
    id_usuario = models.OneToOneField('Usuarios', models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_pelicula = models.ForeignKey('Peliculas', models.DO_NOTHING, db_column='id_pelicula')

    class Meta:
        managed = False
        db_table = 'Favoritas'
        unique_together = (('id_usuario', 'id_pelicula'),)


class Peliculas(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Peliculas'


class Reseñas(models.Model):
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_pelicula = models.ForeignKey(Peliculas, models.DO_NOTHING, db_column='id_pelicula', blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Reseñas'


class Usuarios(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(unique=True, max_length=255, blank=True, null=True)
    contraseña = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuarios'


class Vistas(models.Model):
    id_usuario = models.OneToOneField(Usuarios, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_pelicula = models.ForeignKey(Peliculas, models.DO_NOTHING, db_column='id_pelicula')

    class Meta:
        managed = False
        db_table = 'Vistas'
        unique_together = (('id_usuario', 'id_pelicula'),)
