from django.urls import path, include
from . import views

urlpatterns = [
    path('cards/', views.CardView.as_view(), name='cards'),
    path('cards/<int:card_id>/', views.CardDetailView.as_view(), name='card_detail'),
]
