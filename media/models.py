from django.db import models

class Media(models.Model):
    CATEGORIA_CHOICES = [('MOVIE', 'Filme'), ('GAME', 'Videojogo'), ('BOOK', 'Livro')]
    titulo = models.CharField(max_length=255, default='Untitled')
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES, default='MOVIE')
    # ... outros campos técnicos ...