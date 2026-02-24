from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo


class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    horario = models.TimeField()

    def __str__(self):
        return f"{self.pelicula} - {self.horario}"


class Entrada(models.Model):
    codigo = models.CharField(max_length=20)
    asiento = models.CharField(max_length=10)
    vendido = models.BooleanField(default=False)
    fecha_venta = models.DateTimeField(blank=True, null=True)
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo


class Snack(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nombre