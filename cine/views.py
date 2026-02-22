from django.shortcuts import render
from .models import Pelicula, Funcion

def peliculas_list(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'cine/peliculas_list.html', {
        'peliculas': peliculas
    })


def pelicula_unica(request):
    titulo = request.GET.get('titulo')
    clasificacion = request.GET.get('clasificacion')

    pelicula = None

    if titulo and clasificacion:
        try:
            pelicula = Pelicula.objects.get(
                titulo=titulo,
                clasificacion=clasificacion
            )
        except Pelicula.DoesNotExist:
            pelicula = None

    return render(request, 'cine/pelicula_unica.html', {
        'pelicula': pelicula
    })
def peliculas_contiene(request):
    texto = request.GET.get("texto")
    peliculas = None

    if texto:
        peliculas = Pelicula.objects.filter(titulo__icontains=texto)

    return render(request, 'cine/peliculas_contiene.html', {
        'peliculas': peliculas
    })
def peliculas_termina(request):
    texto = request.GET.get("texto")
    peliculas = None

    if texto:
        peliculas = Pelicula.objects.filter(titulo__iendswith=texto)

    return render(request, 'cine/peliculas_termina.html', {
        'peliculas': peliculas
    })
def funciones_orden_mixto(request):
    funciones = Funcion.objects.all().order_by("estado", "-fecha_hora")
    return render(request, "cine/funciones_orden_mixto.html", {
        "funciones": funciones
    })
def entradas_rango(request):
    entradas = Entrada.objects.all()[4:7]
    return render(request, "cine/entradas_rango.html", {
        "entradas": entradas
    })
from django.shortcuts import render
from .models import Snack

def snacks_prefijo(request):
    prefijo = request.GET.get('prefijo', '')

    snacks = Snack.objects.filter(producto__startswith=prefijo)

    return render(request, 'cine/snacks_prefijo.html', {
        'snacks': snacks,
        'prefijo': prefijo
    })
def snacks_busqueda(request):
    texto = request.GET.get('q', '')

    snacks = Snack.objects.filter(producto__icontains=texto)

    return render(request, 'cine/snacks_busqueda.html', {
        'snacks': snacks,
        'texto': texto
    })
from django.db.models import Q

def snacks_avanzado(request):
    texto = request.GET.get('q', '')
    precio_min = request.GET.get('precio', '')

    snacks = Snack.objects.all()

    if texto:
        snacks = snacks.filter(producto__icontains=texto)

    if precio_min:
        snacks = snacks.filter(precio_unitario__gte=precio_min)

    return render(request, 'cine/snacks_avanzado.html', {
        'snacks': snacks
    })
from django.db.models import Sum, Count

def snacks_resumen(request):
    total_precio = Snack.objects.aggregate(
        total=Sum('precio_unitario')
    )

    total_snacks = Snack.objects.aggregate(
        cantidad=Count('id')
    )

    return render(request, 'cine/snacks_resumen.html', {
        'total_precio': total_precio['total'],
        'total_snacks': total_snacks['cantidad']
    })
from django.db.models import Count

def snacks_por_precio(request):
    resumen = Snack.objects.values('precio_unitario') \
                            .annotate(total=Count('id')) \
                            .order_by('precio_unitario')

    return render(request, 'cine/snacks_por_precio.html', {
        'resumen': resumen
    })
from django.db.models import F

def aumentar_precio(request):
    Snack.objects.update(
        precio_unitario=F('precio_unitario') + 5
    )

    return render(request, 'cine/aumento.html')
def eliminar_baratos(request):
    Snack.objects.filter(precio_unitario__lt=10).delete()
    return render(request, 'cine/eliminado.html')