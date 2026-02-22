from django.shortcuts import render

def lista_peliculas(request):
    return render(request, 'pelicula/lista.html')