from django.shortcuts import render, redirect
from master.models import Reserva
from django.contrib import messages

def home(request):
    grupo= ''
    for g in request.user.groups.all():
        grupo = g.name
    if grupo != 'control':
        if grupo == 'estudiante':
            return redirect('genesis')
        elif grupo == 'admin':
            return redirect('master')
        else:
            return redirect('logout')

    reservas = Reserva.objects.all().order_by('hora').order_by('fecha').order_by('-estado')
    data = {
        'reservas': reservas
    }
    return render(request, 'galileo.html', data)

def cumplir(request, id):
    return cambiar_estado(request, id, 'CUMPLIDA')

def cancelar(request, id):
    return cambiar_estado(request, id, 'NO CUMPLIDA')

def cambiar_estado(request, id, estado):
    try:
        reserva = Reserva.objects.get(pk=id)
        reserva.estado = estado
        reserva.save()
        messages.success(request, 'Reserva actualizada', extra_tags='alert alert-success')
    except:
        messages.success(request, 'No se pudo cancelar la reserva', extra_tags='alert alert-danger')
    return redirect('galileo')