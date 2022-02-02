from django.urls import path, include

from web import views

urlpatterns = [
    path('', views.inicio_view, name="inicio"),
]
