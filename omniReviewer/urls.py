"""
URL configuration for omniReviewer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views # Views prontas de login
from django.urls import include, path
from conta import views as user_views
from django.conf.urls.static import static

from omniReviewer import settings, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar/', user_views.registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='conta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='conta/logout.html'), name='logout'),
    path('reviews/', include('review.urls')),
    path('media/', include('media.urls')),
    path('', include('conta.urls')),
    path('', views.paginaHome, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
