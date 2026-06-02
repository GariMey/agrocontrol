from django.db import models

class Cultivo(models.Model):
    TEMPORADAS = [
        ('PRIMAVERA', 'Primavera'),
        ('VERANO', 'Verano'),
        ('OTOÑO', 'Otoño'),
        ('INVIERNO', 'Invierno'),
        ('TODO_EL_AÑO', 'Todo el año'),
    ]
    
    TIPOS = [
        ('GRANO', 'Grano'),
        ('FRUTA', 'Fruta'),
        ('VERDURA', 'Verdura'),
        ('TUBERCULO', 'Tubérculo'),
        ('LEGUMBRE', 'Legumbre'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='VERDURA')
    region = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    temporada_siembra = models.CharField(max_length=20, choices=TEMPORADAS, default='PRIMAVERA')
    temporada_cosecha = models.CharField(max_length=20, choices=TEMPORADAS, default='VERANO')
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def valor_total(self):
        """Calcula el valor total del cultivo"""
        return self.precio * self.cantidad

# Modelo para Historial de Precios
class HistorialPrecio(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='historial_precios')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.cultivo.nombre} - ${self.precio} ({self.fecha.date()})"