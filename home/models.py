from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Cursos(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    thumb = models.ImageField(upload_to = "thumb_cursos")

    def __str__(self) -> str:
        return self.nome


class Aulas(models.Model):
    nome = models.CharField(max_length = 100)
    descricao = models.TextField()
    aula = models.FileField(upload_to = "aulas")
    curso = models.ForeignKey(Cursos, on_delete = models.DO_NOTHING)


    def __str__(self) -> str:
        return self.nome


class Comentarios(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    aula = models.ForeignKey(Aulas, on_delete=models.DO_NOTHING)
    comentario = models.TextField()
    data = models.DateTimeField(default=datetime.now)
    
    def __str__(self) -> str:
        return self.criado_por.username


class NotasAula(models.Model):
    choices = (
        ('p', 'Péssimo'),
        ('r', 'Ruim'),
        ('re', 'Regular'),
        ('b', 'Bom'),
        ('o', 'Ótimo')
    )

    aula = models.ForeignKey(Aulas, on_delete=models.DO_NOTHING)
    nota = models.CharField(max_length=50, choices=choices)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)