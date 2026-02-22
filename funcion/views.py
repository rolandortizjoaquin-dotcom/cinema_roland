from django.shortcuts import render

def funciones_por_pelicula(request, id):
    pelicula = {
        "id": id,
        "titulo": f"Película {id}"
    }

    funciones = [
        {"hora": "14:00", "precio": 15, "estado": "Disponible"},
        {"hora": "16:00", "precio": 18, "estado": "Agotado"},
        {"hora": "18:00", "precio": 20, "estado": "Disponible"},
        {"hora": "20:00", "precio": 22, "estado": "Disponible"},
        {"hora": "22:00", "precio": 25, "estado": "Disponible"},
    ] * 3  # genera 15 funciones

    return render(request, "funcion/funciones_list.html", {
        "pelicula": pelicula,
        "funciones": funciones
    })