from .models import *
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from django.urls import reverse
import hashlib
import re


def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/cursos')
        else:
            return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Todos os campos devem ser preenchidos.')
            return redirect(reverse('cadastro'))
        
        t = re.compile(r'[a-z0-9_.]+@[a-z0-9-]+\.[a-z]+')
        check_match = t.match(email)
        if not check_match:
            messages.add_message(request, constants.ERROR, 'Digite um email válido.')
            return redirect(reverse('cadastro'))
        
        email_verifica = User.objects.filter(email=email)
        if email_verifica.exists():
            messages.add_message(request, constants.ERROR, 'Email já cadastrado.')
            return redirect(reverse('cadastro'))
        
        if len(senha) < 4:
            messages.add_message(request, constants.ERROR, 'Sua senha deve ter pelo menos 4 caracteres.')
            return redirect(reverse('cadastro'))
        
        if not (senha == confirmar_senha):
            messages.add_message(request, constants.ERROR, 'As senhas devem ser iguais.')
            return redirect(reverse('cadastro'))
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
        user.save()
        
        return redirect(reverse('login'))


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        else:
            return render(request, 'login.html')
        
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(username=username, password=senha)
        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos.')
            return redirect(reverse('login'))
        else:
            auth.login(request, user)
            return redirect(reverse('home'))


def logout(request):
    auth.logout(request)
    messages.add_message(request, constants.INFO, 'Deslogado do sistema com sucesso.')
    return redirect(reverse('login'))
