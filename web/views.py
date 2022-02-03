import random
from datetime import timedelta

import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone

from web.models import Insumo, ReporteInsumo, TIPOS_INSUMO


def obtener_reportes_recientes():
    return ReporteInsumo.objects.select_related("insumo").filter(
        fecha_hora_reporte__gt=timezone.now() - timedelta(days=14)
    )


def geocodificar_direccion(direccion):
    mapquest_key = settings.MAPQUESTAPI_ACCESS_KEY
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={mapquest_key}&location={direccion}"

    response = requests.get(url)

    response_dict = response.json()
    resultados = response_dict["results"]

    if len(resultados) < 1:
        #! Fallback: la API de Mapquest no es muy precisa en Latinoamerica,
        #! y no hay muchas opciones gratuitas para el prototipo.
        #! Si no se encuentra la ubicación, la agregamos a un punto aleatorio
        #! en Caracas.

        # (latitud, longitud)
        puntos_en_caracas = [
            (10.4806, -66.9036),
        ]
        return random.choice(puntos_en_caracas)

    # En este punto, tenemos algún resultado y obtenemos sus coordenadas
    primer_resultado = resultados[0]
    return (
        primer_resultado["latLng"]["lat"],
        primer_resultado["latLng"]["lng"],
    )



def inicio_view(request):
    plantilla = "index.html"

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

        nombre_insumo = data["insumo"].upper()
        tipo = int(data["tipo"])
        insumo, _ = Insumo.objects.get_or_create(
            nombre=nombre_insumo.strip(), tipo=tipo
        )

        costo = data["costo"]
        direccion = data["direccion"]
        referencia = data["referencia"]

        latitud, longitud = geocodificar_direccion(direccion)

        ReporteInsumo.objects.create(
            insumo=insumo,
            tipo=tipo,
            costo=costo,
            direccion=direccion,
            referencia=referencia,
            latitud=latitud,
            longitud=longitud,
        )

        # TODO: mensaje de éxito o error

    return redirect("inicio")
