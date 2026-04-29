from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

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