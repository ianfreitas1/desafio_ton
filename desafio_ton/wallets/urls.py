from django.urls import path, include
from . import views

urlpatterns = [
    path('wallets/', views.WalletView.as_view(), name='wallets'),
    path('wallets/<int:wallet_id>/',
         views.WalletDetailView.as_view(), name='wallet_detail'),
    path('wallets/<int:wallet_id>/cards/',
         views.WalletCardsView.as_view(), name='wallet_cards')
]
