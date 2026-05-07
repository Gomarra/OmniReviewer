from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from media.models import Media
from .forms import ReviewForm

@login_required # Garante que apenas usuários logados comentem (RF 001)
def add_review(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user # Define o autor (RF 003)
            review.media = media # Vincula à mídia atual
            
            # Lógica de Filtro de Conteúdo (RF 010)
            # Por enquanto, salvamos direto. No futuro, adicionamos a verificação automática aqui.
            review.save()
            
            return redirect('media_detail', category=media.category, external_id=media.external_id)
    return redirect('media_detail', category=media.category, external_id=media.external_id)