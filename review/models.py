from django.db import models
from django.contrib.auth.models import User
from media.models import Media  # Importando o modelo do outro app

class Review(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True) # Relaciona com o app media
    conteudo = models.TextField()
    recomendado = models.BooleanField(default=True)
    # ... campos de moderação ...