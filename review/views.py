from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from media.models import Media
from review.models import Review
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

@login_required
def edit_review(request, review_id):
    # Garante que a review existe e pertence ao usuário logado
    review = get_object_or_404(Review, id=review_id, author=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua review foi atualizada!')
            # Redireciona de volta para o perfil do usuário
            return redirect('profile')
    else:
        form = ReviewForm(instance=review)
        
    return render(request, 'review/edit_review.html', {'form': form, 'review': review})