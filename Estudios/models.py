from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la Categoría")

    def __str__(self):
        return self.nombre


class Maquina(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la Máquina")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maquinas", null=True, blank=True)

    def __str__(self):
        return self.nombre

class Tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Tipo de actividad")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tipos", null=True, blank=True)

    def __str__(self):
        return self.nombre

class Area(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre del area")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="areas", null=True, blank=True)

    def __str__(self):
        return self.nombre



class Estudio(models.Model):
    id_estudio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateField()
    tiempo_inicio = models.DateTimeField(null=True, blank=True)
    tiempo_fin = models.DateTimeField(null=True, blank=True)
    duracion = models.DurationField(null=True, blank=True)
    cronometro = models.IntegerField(default=0)
    pausado = models.BooleanField(default=False)
    tiempo_pausa = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, related_name="maquina",on_delete=models.CASCADE, null=True, verbose_name="maquina", )
    area = models.ForeignKey(Area, related_name="area",on_delete=models.CASCADE, null=True, verbose_name="area", )

    def actividades_count(self):
        return self.actividad_set.count()

    def pausar_estudio(self):
        if self.tiempo_inicio and not self.tiempo_fin:
            self.pausado = True
            self.tiempo_pausa = timezone.now()
            # Actualiza la duración cuando se pausa
            self.duracion = self.tiempo_pausa - self.tiempo_inicio
            self.save()

    def reanudar_estudio(self):
        if self.tiempo_inicio and not self.tiempo_fin and self.pausado:
            tiempo_pausado = timezone.now() - self.tiempo_pausa
            self.tiempo_inicio += tiempo_pausado
            self.pausado = False
            self.tiempo_pausa = None
            self.save()



class Actividad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default='#34e610') 
    def vueltas_actividad(self):
        return self.vueltas.all() 


class Vuelta(models.Model):
    id = models.AutoField(primary_key=True)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='vueltas')
    tiempo_vuelta = models.DurationField()
    tiempo_total = models.DurationField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    
    def comentarios_vuelta(self):
        return self.comentarios.all().values_list('contenido', flat=True)
    
    def cantidad_comentarios(self):
        return self.comentarios.count()  
    
    def save(self, *args, **kwargs):
        try:
            ultima_vuelta = self.actividad.vueltas.order_by('-fecha_registro', '-id').first()
            if ultima_vuelta:
                self.tiempo_total = ultima_vuelta.tiempo_total + self.tiempo_vuelta
            else:
                self.tiempo_total = self.tiempo_vuelta 
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error al guardar la vuelta: {e}")
    @property        
    def tiempo_real(self):
        # Filtra las vueltas por usuario y ordena por fecha de registro e id
        vueltas_usuario = Vuelta.objects.filter(usuario=self.usuario).order_by('fecha_registro', 'id')

        # Encuentra el índice de la vuelta actual en la lista ordenada
        indice_actual = list(vueltas_usuario).index(self)

        # Si es el primer registro, devuelve el tiempo total como tiempo real
        if indice_actual == 0:
            return self.tiempo_total

        # Calcula el Tiempo Real usando la fórmula mencionada para las demás vueltas del 
        vuelta_anterior = vueltas_usuario[indice_actual - 1]
        return max(self.tiempo_total - vuelta_anterior.tiempo_total, timedelta())
    
class Comentario2(models.Model):
    vuelta = models.ForeignKey(Vuelta, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
     
class ArchivoCompartido(models.Model):
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos_compartidos/', blank=True, null=True)

