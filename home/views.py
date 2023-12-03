from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import json


def home(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.add_message(request, constants.ERROR, 'Faça login antes de acessar a plataforma.')
            return redirect(reverse('login'))
        else:
            cursos = Cursos.objects.all()
            usuario = request.user
            return render(request, 'home.html', {
                'cursos':cursos,
                'usuario': usuario,
            }
                          )


def curso(request, id):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.add_message(request, constants.ERROR, 'Faça login antes de acessar a plataforma.')
            return redirect(reverse('login'))
        else:
            aulas = Aulas.objects.filter(curso=id)
            usuario = request.user
            return render(request, 'curso.html', {
                'aulas':aulas,
                'usuario': usuario,
            }
                          )


def aula(request, id):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.add_message(request, constants.ERROR, 'Faça login antes de acessar a plataforma.')
            return redirect(reverse('login'))
        else:
            aula = Aulas.objects.get(id=id)
            usuario = request.user
            comentarios = Comentarios.objects.filter(aula = aula).order_by('-data')
            
            usuario_avaliou = NotasAula.objects.filter(aula_id = id).filter(usuario_id = usuario.id)
            avaliacoes = NotasAula.objects.filter(aula_id = id)
        
            return render(request, 'aula.html', {
                'aula': aula,
                'usuario': usuario,
                'comentarios': comentarios,
                'usuario_avaliou': usuario_avaliou,
                'avaliacoes': avaliacoes,
            }
                          )


def comentarios(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.add_message(request, constants.ERROR, 'Faça login antes de acessar a plataforma.')
            return redirect(reverse('login'))
    else:
        usuario_id = request.POST.get('usuario_id')
        comentario = request.POST.get('comentario')
        aula_id = request.POST.get('aula_id')
        
        comentario_instancia = Comentarios(
            usuario_id = usuario_id,
            aula_id = aula_id,
            comentario = comentario
        )
        comentario_instancia.save()
        
        comentarios = Comentarios.objects.filter(aula=aula_id).order_by('-data')
        somente_nomes = [i.usuario.username for i in comentarios]
        somente_comentarios = [i.comentario for i in comentarios]
        comentarios = list(zip(somente_nomes, somente_comentarios))
        
        return HttpResponse(json.dumps(
            {
                'status':'1',
                'comentarios':comentarios,
            }
        )
        )


def processa_avaliacao(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.add_message(request, constants.ERROR, 'Faça login antes de acessar a plataforma.')
            return redirect(reverse('login'))
    else:
        avaliacao = request.POST.get('avaliacao')
        aula_id = request.POST.get('aula_id')
        usuario_id = request.user.id
        
        usuario_avaliou = NotasAula.objects.filter(aula_id=aula_id).filter(usuario_id=usuario_id)
        if not usuario_avaliou:
            notas_aula = NotasAula(
                aula_id = aula_id,
                nota = avaliacao,
                usuario_id=request.user.id,
            )
            notas_aula.save()
            
            return redirect(f'aula/{aula_id}')
