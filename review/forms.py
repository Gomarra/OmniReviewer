from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'recommended']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Escreva sua review aqui...',
                'rows': 5,
                'style': 'width: 100%; border-radius: 5px; padding: 10px;'
            }),
        }
        labels = {
            'content': 'Sua Análise',
            'recommended': 'Você recomenda esta mídia?',
        }