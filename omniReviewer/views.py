from django.shortcuts import render

from media.models import Media

def paginaInicial(request):
  # 1. Buscamos todas as mídias do banco local
    todas_as_midias = Media.objects.all()
    
    midias_populares = []
    
    # 2. Varremos cada mídia para calcular manualmente quem tem boas notas
    for media in todas_as_midias:
        total = media.reviews.filter(is_approved=True).count()
        
        # Só recomendamos mídias que tenham pelo menos uma avaliação
        if total > 0:
            positivas = media.reviews.filter(is_approved=True, recommended=True).count()
            porcentagem = (positivas / total) * 100
            
            # Se a aprovação for de 70% para cima, ela entra na nossa lista
            if porcentagem >= 70:
                # Guardamos a mídia e a porcentagem juntas para usar na tela
                midias_populares.append({
                    'objeto': media,
                    'porcentagem': int(porcentagem)
                })
    
    # 3. Ordenamos a lista para que as maiores porcentagens apareçam primeiro
    midias_populares = sorted(midias_populares, key=lambda x: x['porcentagem'], reverse=True)[:6]

    # 4. Entregamos o resultado para o arquivo HTML dentro de um "Dicionário" (Contexto)
    return render(request, 'home.html', {'lista_recomendados': midias_populares})