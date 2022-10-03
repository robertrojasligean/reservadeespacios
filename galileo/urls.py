from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='galileo'),
    path('cancelar-reserva/<int:id>', views.cancelar, name='cancelar-reserva-galileo'),
    path('cumplir-reserva/<int:id>', views.cumplir, name='cumplir-reserva-galileo'),
]
