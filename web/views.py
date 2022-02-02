from datetime import timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone

from web.models import Insumo, ReporteInsumo, TIPOS_INSUMO

def obtener_reportes_recientes():
    return ReporteInsumo.objects.select_related("insumo").filter(
        fecha_hora_reporte__gt=timezone.now() - timedelta(days=14)
    )


def inicio_view(request):
    plantilla = "inicio.html"

    insumos = Insumo.objects.all()
    reportes = obtener_reportes_recientes()

    # Filtrado
    if request.method == "POST":
        data = request.POST

        nombre = data.get("nombre")
        if nombre:
            reportes = reportes.filter(insumo__nombre=nombre.strip())

        tipo = int(data.get("tipo", 0))
        if tipo > 0:
            reportes = reportes.filter(insumo__tipo=tipo)

        # TODO: Mensaje que indique que estás filtrando

    datos = {
        "reportes": reportes,
        "insumos": insumos,
        "tipos_insumo": TIPOS_INSUMO,
        "mapbox_api_key": settings.MAPBOX_API_KEY,
    }

    return render(request, plantilla, datos)


def agregar_reporte_view(request):
    if request.method == "POST":
        # Esto podría hacerse con los Forms de Django, pero
        # así sale relativamente más rápido para un MVP
        data = request.POST
        insumo_id = data["insumo_id"]
        tipo = data["tipo"]
        costo = data["costo"]
        referencia = data["referencia"]
        latitud = data["latitud"]
        longitud = data["longitud"]

        ReporteInsumo.objects.create(
            insumo_id=insumo_id,
            tipo=tipo,
            costo=costo,
            referencia=referencia,
            latitud=latitud,
            longitud=longitud,
        )

        # TODO: mensaje de éxito o error

    return redirect("inicio")
