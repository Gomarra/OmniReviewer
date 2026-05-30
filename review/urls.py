from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:media_id>/', views.add_review, name='add_review'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
]