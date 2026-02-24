from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Pelicula, Funcion, Entrada, Snack
from .serializers import (
    PeliculaSerializer,
    FuncionSerializer,
    EntradaSerializer,
    SnackSerializer
)

# =====================================================
# VISTAS TRADICIONALES (FUNCIONES)
# =====================================================

def peliculas_list(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'cine/peliculas_list.html', {'peliculas': peliculas})


def pelicula_unica(request):
    titulo = request.GET.get('titulo')
    pelicula = None

    if titulo:
        try:
            pelicula = Pelicula.objects.get(titulo=titulo)
        except Pelicula.DoesNotExist:
            pelicula = None

    return render(request, 'cine/pelicula_unica.html', {'pelicula': pelicula})


def peliculas_contiene(request):
    texto = request.GET.get("texto")
    peliculas = None

    if texto:
        peliculas = Pelicula.objects.filter(titulo__icontains=texto)

    return render(request, 'cine/peliculas_contiene.html', {'peliculas': peliculas})


def peliculas_termina(request):
    texto = request.GET.get("texto")
    peliculas = None

    if texto:
        peliculas = Pelicula.objects.filter(titulo__iendswith=texto)

    return render(request, 'cine/peliculas_termina.html', {'peliculas': peliculas})


def funciones_orden_mixto(request):
    funciones = Funcion.objects.all().order_by("-horario")
    return render(request, "cine/funciones_orden_mixto.html", {"funciones": funciones})


def entradas_rango(request):
    entradas = Entrada.objects.all()[4:7]
    return render(request, "cine/entradas_rango.html", {"entradas": entradas})


def snacks_prefijo(request):
    prefijo = request.GET.get('prefijo', '')
    snacks = Snack.objects.filter(nombre__startswith=prefijo)
    return render(request, 'cine/snacks_prefijo.html', {'snacks': snacks})


def snacks_busqueda(request):
    texto = request.GET.get('q', '')
    snacks = Snack.objects.filter(nombre__icontains=texto)
    return render(request, 'cine/snacks_busqueda.html', {'snacks': snacks})


def snacks_avanzado(request):
    texto = request.GET.get('q', '')
    precio_min = request.GET.get('precio', '')

    snacks = Snack.objects.all()

    if texto:
        snacks = snacks.filter(nombre__icontains=texto)

    if precio_min:
        snacks = snacks.filter(precio__gte=precio_min)

    return render(request, 'cine/snacks_avanzado.html', {'snacks': snacks})


def snacks_resumen(request):
    total_precio = Snack.objects.aggregate(total=Sum('precio'))
    total_snacks = Snack.objects.aggregate(cantidad=Count('id'))

    return render(request, 'cine/snacks_resumen.html', {
        'total_precio': total_precio['total'],
        'total_snacks': total_snacks['cantidad']
    })


def snacks_por_precio(request):
    resumen = Snack.objects.values('precio') \
                           .annotate(total=Count('id')) \
                           .order_by('precio')

    return render(request, 'cine/snacks_por_precio.html', {'resumen': resumen})


def aumentar_precio(request):
    Snack.objects.update(precio=F('precio') + 5)
    return render(request, 'cine/aumento.html')


def eliminar_baratos(request):
    Snack.objects.filter(precio__lt=10).delete()
    return render(request, 'cine/eliminado.html')


# =====================================================
# CLASS BASED VIEWS (CRUD TRADICIONAL)
# =====================================================

class PeliculaList(ListView):
    model = Pelicula
    template_name = 'cine/pelicula_list_vc.html'
    context_object_name = 'peliculas'


class PeliculaCreate(CreateView):
    model = Pelicula
    fields = ['titulo']
    template_name = 'cine/pelicula_form.html'
    success_url = reverse_lazy('pelicula_list_vc')


class PeliculaUpdate(UpdateView):
    model = Pelicula
    fields = ['titulo']
    template_name = 'cine/pelicula_form.html'
    success_url = reverse_lazy('pelicula_list_vc')


class PeliculaDelete(DeleteView):
    model = Pelicula
    template_name = 'cine/pelicula_confirm_delete.html'
    success_url = reverse_lazy('pelicula_list_vc')


# =====================================================
# API REST FRAMEWORK
# =====================================================

# =====================================================
# ENDPOINT PERSONALIZADO - TOP VENDIDAS
# =====================================================

# =====================================================
# API REST FRAMEWORK
# =====================================================

class PeliculaListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        titulo = request.GET.get('titulo')
        peliculas = Pelicula.objects.all()

        if titulo:
            peliculas = peliculas.filter(titulo__icontains=titulo)

        serializer = PeliculaSerializer(peliculas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PeliculaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class FuncionListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        funciones = Funcion.objects.all()
        serializer = FuncionSerializer(funciones, many=True)
        return Response(serializer.data)


class EntradaListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entradas = Entrada.objects.all()
        serializer = EntradaSerializer(entradas, many=True)
        return Response(serializer.data)


class SnackListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nombre = request.GET.get('nombre')
        snacks = Snack.objects.all()

        if nombre:
            snacks = snacks.filter(nombre__icontains=nombre)

        serializer = SnackSerializer(snacks, many=True)
        return Response(serializer.data)


# =====================================================
# ENDPOINT PERSONALIZADO - TOP VENDIDAS
# =====================================================

# =====================================================
# ENDPOINT PERSONALIZADO - TOP VENDIDAS
# =====================================================

class PeliculasTopVendidasAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        peliculas = (
            Pelicula.objects
            .annotate(total_entradas_vendidas=Sum('entrada__cantidad'))
            .filter(total_entradas_vendidas__gt=0)
            .order_by('-total_entradas_vendidas')
            .values('titulo', 'genero', 'total_entradas_vendidas')
        )

        return Response(peliculas)


# =====================================================
# ENDPOINT PERSONALIZADO - ACTUALIZAR PRECIOS
# =====================================================

class ActualizarPreciosSnacksAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        descuento = request.data.get('descuento')

        if descuento is None:
            return Response(
                {"error": "Debe enviar el campo descuento"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            descuento = float(descuento)
        except ValueError:
            return Response(
                {"error": "Descuento debe ser numérico"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Snack.objects.filter(precio__lt=descuento).exists():
            return Response(
                {"error": "El descuento es mayor que el precio de algunos snacks"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Snack.objects.update(precio=F('precio') - descuento)

        snacks_actualizados = Snack.objects.all()
        serializer = SnackSerializer(snacks_actualizados, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)