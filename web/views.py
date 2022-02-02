from datetime import timedelta

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from web.models import ReporteInsumo

def obtener_reportes_recientes():
    return ReporteInsumo.objects.select_related("insumo").filter(
        fecha_hora_reporte__gt=timezone.now() - timedelta(days=14)
    )


def inicio_view(request):
    plantilla = "inicio.html"

    reportes = obtener_reportes_recientes()
    datos = {
        "reportes": reportes,
        "mapbox_api_key": settings.MAPBOX_API_KEY,
    }

    return render(request, plantilla, datos)
