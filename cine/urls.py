from django.urls import path
from . import views
from .views import (
    PeliculaListAPI,
    FuncionListAPI,
    EntradaListAPI,
    SnackListAPI,
    PeliculasTopVendidasAPI,
    ActualizarPreciosSnacksAPI,
    PeliculaList,
    PeliculaCreate,
    PeliculaUpdate,
    PeliculaDelete
)

urlpatterns = [

    # ======================
    # API REST
    # ======================
    path('api/peliculas/', PeliculaListAPI.as_view(), name='api_peliculas'),
    path('api/funciones/', FuncionListAPI.as_view(), name='api_funciones'),
    path('api/entradas/', EntradaListAPI.as_view(), name='api_entradas'),
    path('api/snacks/', SnackListAPI.as_view(), name='api_snacks'),
    path('api/peliculas/top-vendidas/', PeliculasTopVendidasAPI.as_view(), name='api_top_vendidas'),
    path('api/snacks/actualizar-precios/', ActualizarPreciosSnacksAPI.as_view(), name='actualizar_precios'),

    # ======================
    # CRUD con Class Based Views
    # ======================
    path('peliculas-vc/', PeliculaList.as_view(), name='pelicula_list_vc'),
    path('peliculas-vc/nueva/', PeliculaCreate.as_view(), name='pelicula_create'),
    path('peliculas-vc/<int:pk>/editar/', PeliculaUpdate.as_view(), name='pelicula_update'),
    path('peliculas-vc/<int:pk>/eliminar/', PeliculaDelete.as_view(), name='pelicula_delete'),

    # ======================
    # Templates normales
    # ======================
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