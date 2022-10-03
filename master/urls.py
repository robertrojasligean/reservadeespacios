from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='master'),
    path('nuevo', views.nuevo, name='nuevo-espacio-reserva'),
    path('editar/<int:id>', views.editar, name='editar-espacio-reserva'),
    path('guardar-nuevo', views.guardar_nuevo, name='guardar-nuevo-espacio-reserva'),
    path('guardar-espacio-reserva/<int:id>', views.guardar, name='guardar-espacio-reserva'),
    path('borrar-espacio-reserva/<int:id>', views.borrar, name='borrar-espacio-reserva'),
]
