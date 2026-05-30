from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='pfp/default.png', upload_to='pfp/profile_pics')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

    # Método opcional para redimensionar fotos grandes e economizar espaço // IA
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
        except (FileNotFoundError, OSError):
            return
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)