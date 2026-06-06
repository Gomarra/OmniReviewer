from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_media, name='search_media'),
    path('detail/<str:category>/<int:external_id>/', views.media_detail, name='media_detail'),
    path('list/update/<int:media_id>/', views.update_list_status, name='update_list_status'),
]