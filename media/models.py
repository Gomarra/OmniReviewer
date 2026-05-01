from django.db import models

class Media(models.Model):
    CATEGORY_CHOICES = [
        ('MOVIE', 'Filme'),
        ('GAME', 'Videojogo'),
        ('BOOK', 'Livro'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    synopsis = models.TextField(blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    external_id = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_approval_rating(self):
        # Esta função busca as review relacionadas no outro app
        total_reviews = self.reviews.filter(is_approved=True).count()
        if total_reviews == 0:
            return "Sem avaliações"
        
        positive_review = self.review.filter(is_approved=True, recommended=True).count()
        percentage = (positive_review / total_reviews) * 100

        if percentage >= 90: return f"Fortemente recomendado ({percentage:.0f}%)"
        elif percentage >= 70: return f"Recomendado ({percentage:.0f}%)"
        elif percentage >= 50: return f"Misto ({percentage:.0f}%)"
        else: return f"Não recomendado ({percentage:.0f}%)"