from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from media.models import UserList
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from review.models import Review
from django.contrib.auth.models import User

def registrar(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Você já pode fazer login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'conta/registrar.html', {'form': form})

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    # Organiza as listas por status para o usuário logado
    user_lists = UserList.objects.filter(user=request.user).select_related('media')
    
    listas_organizadas = {
        'PLAN_TO': [item.media for item in user_lists if item.status == 'PLAN_TO'],
        'WATCHING': [item.media for item in user_lists if item.status == 'WATCHING'],
        'COMPLETED': [item.media for item in user_lists if item.status == 'COMPLETED'],
        'DROPPED': [item.media for item in user_lists if item.status == 'DROPPED'],
    }

    user_reviews = Review.objects.filter(author=request.user).order_by('-created_at')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'listas': listas_organizadas,
        'reviews': user_reviews
    }
    return render(request, 'conta/profile.html', context)

def public_profile(request, username):
    """Exibe o perfil para outros usuários (sem formulários de edição)"""
    person = get_object_or_404(User, username=username)
    user_lists = UserList.objects.filter(user=person).select_related('media')
    
    listas_organizadas = {
        'PLAN_TO': [item.media for item in user_lists if item.status == 'PLAN_TO'],
        'WATCHING': [item.media for item in user_lists if item.status == 'WATCHING'],
        'COMPLETED': [item.media for item in user_lists if item.status == 'COMPLETED'],
        'DROPPED': [item.media for item in user_lists if item.status == 'DROPPED'],
    }
    
    reviews = Review.objects.filter(author=person, is_approved=True).order_by('-created_at')

    return render(request, 'conta/public_profile.html', {
        'person': person,
        'listas': listas_organizadas,
        'reviews': reviews
    })