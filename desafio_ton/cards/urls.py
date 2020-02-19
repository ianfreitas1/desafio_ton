from django.urls import path, include
from . import views

urlpatterns = [
    path('cards/', views.CardView.as_view(), name='cards')
]
