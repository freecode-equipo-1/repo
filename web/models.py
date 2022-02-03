from django.db import models

TIPO_INSUMO_MEDICAMENTO = 1
TIPO_INSUMO_EXAMEN = 2
TIPO_INSUMO_OPERACION = 3
TIPO_INSUMO_PSICOLOGICO = 4
TIPOS_INSUMO = (
    (TIPO_INSUMO_MEDICAMENTO, "Medicamento"),
    (TIPO_INSUMO_EXAMEN, "Examen"),
    (TIPO_INSUMO_OPERACION, "Operación"),
    (TIPO_INSUMO_PSICOLOGICO, "Ayuda Psicológica"),
)


class Insumo(models.Model):
    """
    Un insumo representa algún tipo de producto o servicio
    que los usuarios pueden buscar en la plataforma.
    """

    nombre = models.CharField(max_length=128, unique=True)
    tipo = models.IntegerField(choices=TIPOS_INSUMO)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


TIPO_REPORTE_NO_VERIFICADO = 1
TIPO_REPORTE_VERIFICADO = 2
TIPO_REPORTE_OFICIAL = 3
TIPOS_REPORTE = (
    (TIPO_REPORTE_NO_VERIFICADO, "No Verificado"),
    (TIPO_REPORTE_VERIFICADO, "Verificado"),
    (TIPO_REPORTE_OFICIAL, "Oficial"),
)

class ReporteInsumo(models.Model):
    """
    Un reporte de insumo representa un reporte específico de disponibilidad
    de uno de los insumos, incluyendo su ubicación y su precio.
    """

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    tipo = models.IntegerField(choices=TIPOS_INSUMO)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    referencia = models.TextField()
    latitud = models.DecimalField(max_digits=10, decimal_places=7)
    longitud = models.DecimalField(max_digits=10, decimal_places=7)

    fecha_hora_reporte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.insumo.nombre} ({self.fecha_hora_reporte})"
