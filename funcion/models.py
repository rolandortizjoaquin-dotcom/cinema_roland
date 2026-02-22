class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)