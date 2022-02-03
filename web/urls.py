from django.urls import path, include

from web import views

urlpatterns = [
    path('faqs', views.faqs_view, name="faqs"),
    path('reportes/agregar', views.agregar_reporte_view, name="agregar-reporte"),
    path('', views.inicio_view, name="inicio"),
]
