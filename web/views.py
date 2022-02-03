import random
from datetime import timedelta

import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone

from web.models import TIPOS_INSUMO, TIPO_REPORTE_NO_VERIFICADO, Insumo, ReporteInsumo


def obtener_reportes_recientes():
    """
    Retorna un queryset con los reportes realizados en los últimos
    14 días.
    """

    return ReporteInsumo.objects.select_related("insumo").filter(
        fecha_hora_reporte__gt=timezone.now() - timedelta(days=14)
    )


def geocodificar_direccion(direccion):
    """
    Busca una dirección textual en la API de Geocodificación de
    Mapquest y retorna su latitud y longitud.
    """

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
            (10.4821246, -66.8449624),
            (10.4833701, -66.8498913),
        ]
        return random.choice(puntos_en_caracas)

    # En este punto, tenemos algún resultado y obtenemos las coordenadas
    # del primero
    primer_resultado = resultados[0]["locations"][0]
    return (
        primer_resultado["latLng"]["lat"],
        primer_resultado["latLng"]["lng"],
    )


def inicio_view(request):
    """
    Controlador de la vista base: muestra el mapa y el buscador,
    y maneja posibles filtros
    """

    plantilla = "index.html"

    insumos = Insumo.objects.all()
    reportes = obtener_reportes_recientes()

    # Filtrado
    nombre = ""
    tipo = 0
    if request.method == "POST":
        data = request.POST

        nombre = data.get("nombre", "")
        if nombre:
            reportes = reportes.filter(insumo__nombre__icontains=nombre.strip())

        tipo = int(data.get("tipo", 0))
        if tipo > 0:
            reportes = reportes.filter(insumo__tipo=tipo)

    datos = {
        "reportes": reportes,
        "insumos": insumos,
        "nombre_filtro": nombre,
        "tipo_filtro": tipo,
        "tipos_insumo": TIPOS_INSUMO,
        "mapbox_api_key": settings.MAPBOX_API_KEY,
    }

    return render(request, plantilla, datos)


def agregar_reporte_view(request):
    """
    Controlador para manejar el formulario de agregar un reporte
    sobre un insumo. Crea el registro en la base de datos y retorna
    el buscador nuevamente.
    """

    if request.method == "POST":
        # Esto podría hacerse con los Forms de Django, pero
        # así sale relativamente más rápido para un MVP
        data = request.POST

        # Obtenemos o creamos el insumo
        nombre_insumo = data["insumo"].upper()
        tipo = int(data["tipo"])
        insumo, _ = Insumo.objects.get_or_create(
            nombre=nombre_insumo.strip(), tipo=tipo
        )

        costo = data["costo"]

        # Ubicación
        direccion = data["direccion"]
        referencia = data["referencia"]
        latitud, longitud = geocodificar_direccion(direccion)

        # Creamos el reporte
        ReporteInsumo.objects.create(
            insumo=insumo,
            tipo=TIPO_REPORTE_NO_VERIFICADO,
            costo=costo,
            direccion=direccion,
            referencia=referencia,
            latitud=latitud,
            longitud=longitud,
        )

        # TODO: mensaje de éxito o error

    return redirect("inicio")
