from django.shortcuts import render, redirect
from master.models import Reserva, EspacioReserva, Estudiante
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
import traceback

def home(request):
    grupo= ''
    for g in request.user.groups.all():
        grupo = g.name
    if grupo != 'estudiante':
        if grupo == 'control':
            return redirect('control')
        elif grupo == 'admin':
            return redirect('master')
        else:
            return redirect('logout')

    user = Estudiante.objects.get(codigo=request.user.username)
    reservas = Reserva.objects.filter(estudiante=user.id).order_by('hora').order_by('fecha').order_by('-estado')
    data = {
        'reservas': reservas
    }
    return render(request, 'genesis.html', data)

def nuevo(request):
    horas = []
    for hora in range(6,21):
        horas.append(dict(id=hora, hora=str(hora)+':00'))
    espacios_r = EspacioReserva.objects.all()
    hoy = date.today()
    hoy = hoy.strftime("%Y-%m-%d 00:00:00.000 -0500")
    data = {
        'espacios_r': espacios_r,
        'horas': horas,
        'hoy': hoy
    }
    return render(request, 'nueva-reserva.html', data)

def cancelar(request, id):
    try:
        reserva = Reserva.objects.get(pk=id)
        reserva.estado = 'CANCELADA'
        reserva.save()
        messages.success(request, 'Reserva cancelada', extra_tags='alert alert-success')
    except:
        messages.success(request, 'No se pudo cancelar la reserva', extra_tags='alert alert-danger')
    return redirect('genesis')

def crear(request):
    try:
        user = Estudiante.objects.get(codigo=request.user.username)
        espacio_reserva_id  = request.POST['espacio_reserva_id']
        espacio_reserva = EspacioReserva.objects.get(pk=espacio_reserva_id)
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        reservas = Reserva.objects.filter(fecha=fecha, hora=hora, estado='PENDIENTE')
        if reservas.count() >= espacio_reserva.aforo:
            messages.success(request, 'El aforo del espacio se alcanzó', extra_tags='alert alert-danger')
            return redirect('nueva-reserva')
        reserva = Reserva()
        reserva.espacio_reserva_id = espacio_reserva_id
        reserva.estudiante_id = user.id
        reserva.fecha = fecha
        reserva.hora = hora
        reserva.estado = 'PENDIENTE'
        reserva.save()
        messages.success(request, 'Reserva creada', extra_tags='alert alert-success')
        return redirect('genesis')
    except Exception as e:
        print(traceback.format_exc())
        messages.success(request, 'No se pudo crear la reserva', extra_tags='alert alert-danger')
        return redirect('nueva-reserva')