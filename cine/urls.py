from django.urls import path
from . import views

urlpatterns = [
    path('peliculas/', views.peliculas_list, name='peliculas_list'),
    path('peliculas/unica/', views.pelicula_unica, name='pelicula_unica'),
    path('peliculas/contiene/', views.peliculas_contiene, name='peliculas_contiene'),
    path('peliculas/termina/', views.peliculas_termina, name='peliculas_termina'),

    path('funciones/orden-mixto/', views.funciones_orden_mixto, name='funciones_orden_mixto'),
    path('entradas/rango/', views.entradas_rango, name='entradas_rango'),
    path('snacks/prefijo/', views.snacks_prefijo, name='snacks_prefijo'),
    path('snacks/busqueda/', views.snacks_busqueda, name='snacks_busqueda'),
    path('snacks/avanzado/', views.snacks_avanzado, name='snacks_avanzado'),
    path('snacks/resumen/', views.snacks_resumen, name='snacks_resumen'),
    path('snacks/por-precio/', views.snacks_por_precio, name='snacks_por_precio'),
    path('snacks/aumentar/', views.aumentar_precio, name='aumentar_precio'),
    path('snacks/eliminar-baratos/', views.eliminar_baratos, name='eliminar_baratos'),
]