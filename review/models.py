from django.db import models
from django.contrib.auth.models import User
from media.models import Media  # Importando o modelo do outro app

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    # Certifique-se de que o related_name seja 'reviews'
    media = models.ForeignKey('media.Media', on_delete=models.CASCADE, related_name='reviews')
    
    content = models.TextField()
    recommended = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    # ... outros campos ...