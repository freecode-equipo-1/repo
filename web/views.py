from django.shortcuts import render


def inicio_view(request):
    plantilla = "inicio.html"
    return render(request, plantilla)
