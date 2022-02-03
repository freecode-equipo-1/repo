from django.urls import path, include

from web import views

urlpatterns = [
    path('', views.inicio_view, name="inicio"),
    path('reportes/agregar', views.agregar_reporte_view, name="agregar-reporte"),
]
