from rest_framework import serializers
from .models import Pelicula, Funcion, Entrada, Snack


class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = ['id', 'titulo']


class FuncionSerializer(serializers.ModelSerializer):
    pelicula_titulo = serializers.CharField(source='pelicula.titulo', read_only=True)

    class Meta:
        model = Funcion
        fields = ['id', 'horario', 'pelicula_titulo']


class FuncionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcion
        fields = ['id', 'horario']


class EntradaSerializer(serializers.ModelSerializer):
    funcion = FuncionSimpleSerializer(read_only=True)
    pelicula = serializers.CharField(source='funcion.pelicula.titulo', read_only=True)

    class Meta:
        model = Entrada
        fields = [
            'id',
            'codigo',
            'asiento',
            'vendido',
            'fecha_venta',
            'funcion',
            'pelicula'
        ]


class SnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = ['id', 'nombre', 'precio']