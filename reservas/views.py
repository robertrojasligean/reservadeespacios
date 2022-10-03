from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from master.models import Espacio, Estudiante

def home(request):
    return render(request, 'index.html')

def login_view(request):
    user = authenticate(
        username=request.POST['username'], 
        password=request.POST['password'])
    grupo = ''
    if user is not None:
        login(request, user)
    else:
        messages.success(
            request,
            'Usuario o contraseña equivocados',
            extra_tags='alert alert-success')
        return redirect('home')

    for g in user.groups.all():
        grupo = g.name
    if grupo == 'estudiante':
        return redirect('genesis')
    elif grupo == 'admin':
        return redirect('master')
    else:
        return redirect('galileo')

def logout_view(request):
    logout(request)
    return redirect('home')


def crear_datos(request):
    Espacio.objects.all().delete()
    espacios = [
        {'nombre': 'LABORATORIO 101', 'tipo': 'LABORATORIO'},
        {'nombre': 'AULA 101', 'tipo': 'AULA'},
        {'nombre': 'BIBLIOTECA 101', 'tipo': 'BIBLIOTECA'},]
    for espacio in espacios:
        new_espacio = Espacio()
        new_espacio.nombre = espacio['nombre']
        new_espacio.tipo = espacio['tipo']
        new_espacio.save()
    Group.objects.all().delete()
    grupos = ['admin', 'control', 'estudiante']
    grupos_id = []
    for grupo in grupos:
        g = Group()
        g.name = grupo
        g.save()
        grupos_id.append(g.id)
    User.objects.all().delete()
    usuarios = [
        {'username': 'admin', 'rol': 0},
        {'username': 'control', 'rol': 1},
        {'username': '1001', 'rol': 2},
        {'username': '2001', 'rol': 2},
    ]
    for usuario in usuarios:
        user = User.objects.create_user(
            usuario['username'], 
            usuario['username']+'@udes.com',
            '123')
        user.groups.set([grupos_id[usuario['rol']]])
        user.save()

    Estudiante.objects.all().delete()
    estudiantes = [
        {'codigo': '1001', 'nombre': 'ROBERT', 'carrera': 'INGENIERIA DE SISTEMAS'},
        {'codigo': '2001', 'nombre': 'ANYELY', 'carrera': 'MEDICINA'},
    ]
    for estudiante in estudiantes:
        nuevo_estudiante = Estudiante()
        nuevo_estudiante.codigo = estudiante['codigo']
        nuevo_estudiante.nombre = estudiante['nombre']
        nuevo_estudiante.carrera = estudiante['carrera']
        nuevo_estudiante.save()

    return render(request, 'index.html')