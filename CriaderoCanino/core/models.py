from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asesor(models.Model):
    codigo=models.CharField(max_length=10,primary_key=True)
    nombre=models.CharField(max_length=100)
    telefono=models.CharField(max_length=10)
    correo=models.CharField(max_length=100)
    mascota=models.ManyToManyField("Mascota", blank = True, related_name = "Asesor")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Asesor")

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    raza = models.CharField(max_length = 20) #Anteriormente era nombre
    tamaño = models.CharField(max_length = 10) #Campo nuevo
    precio =models.IntegerField(default = 0) #Campo nuevo
    foto = models.ImageField(upload_to ='mascotas', null = True, blank = True) #Foto del perro
    asesor = models.ForeignKey(Asesor,models.CASCADE, related_name="mascotas")
    descripcion = models.TextField() #Descripcion del perro
    comprado = models.CharField(max_length = 200, null = True, blank = True)

    def __str__(self):
        return self.raza