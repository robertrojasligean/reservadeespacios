from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='genesis'),
    path('nuevo', views.nuevo, name='nueva-reserva'),
    path('cancelar-reserva/<int:id>', views.cancelar, name='cancelar-reserva'),
    path('crear-reserva', views.crear, name='crear-reserva'),
]
