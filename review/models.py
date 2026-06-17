from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    media = models.ForeignKey('media.Media', on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    content = models.TextField()
    recommended = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)