from django.shortcuts import render, redirect
from .models import EspacioReserva, Espacio
from django.contrib import messages

def home(request):
    grupo= ''
    for g in request.user.groups.all():
        grupo = g.name
    if grupo != 'admin':
        if grupo == 'control':
            return redirect('control')
        elif grupo == 'estudiante':
            return redirect('genesis')
        else:
            return redirect('logout')
    espacio_reservas = EspacioReserva.objects.all()
    return render(request, 'master.html', {'data': espacio_reservas})


def nuevo(request):
    grupo= ''
    for g in request.user.groups.all():
        grupo = g.name
    if grupo != 'admin':
        if grupo == 'control':
            return redirect('control')
        elif grupo == 'estudiante':
            return redirect('genesis')
        else:
            return redirect('logout')
    espacios_usados = EspacioReserva.objects.all().values_list('espacio')
    espacios = Espacio.objects.exclude(id__in=espacios_usados)
    data = {
        'espacios': espacios,
    }
    return render(request, 'nuevo.html', data)

def editar(request, id):
    check_group(request)
    espacio_reserva = EspacioReserva.objects.get(pk=id)
    espacios_usados = EspacioReserva.objects.all().values_list('espacio')
    espacios = Espacio.objects.exclude(id__in=espacios_usados)
    data = {
        'espacios': espacios,
        'espacio_r': espacio_reserva
    }    
    return render(request, 'editar.html', data)

def guardar_nuevo(request):
    try:
        espacio_reserva = EspacioReserva()
        espacio_reserva.espacio = Espacio(id=request.POST['espacio'])
        espacio_reserva.horasmaxreserva = request.POST['horasmaxreserva']
        espacio_reserva.aforo = request.POST['aforo']
        espacio_reserva.habilitado = request.POST['habilitado']
        espacio_reserva.save()
        messages.success(request, 'Espacio agregado', extra_tags='alert alert-success')
        return redirect('master')
    except:
        messages.success(request, 'No se pudo crear el espacio', extra_tags='alert alert-danger')
        return redirect('nuevo')

def guardar(request, id):
    try:
        espacio_reserva = EspacioReserva.objects.get(pk=id)
        espacio_reserva.espacio = Espacio(id=request.POST['espacio'])
        espacio_reserva.horasmaxreserva = request.POST['horasmaxreserva']
        espacio_reserva.aforo = request.POST['aforo']
        espacio_reserva.habilitado = request.POST['habilitado']
        espacio_reserva.save()
        messages.success(request, 'Espacio guardado', extra_tags='alert alert-success')
        return redirect('master')
    except:
        messages.success(request, 'No se pudo guardar el espacio', extra_tags='alert alert-danger')
        return redirect('nuevo')

def borrar(request, id):
    try:
        EspacioReserva.objects.get(pk=id).delete()
        messages.success(request, 'Espacio borrado', extra_tags='alert alert-success')
    except:
        messages.success(request, 'No se pudo borrar el espacio', extra_tags='alert alert-danger')
    return redirect('master')
