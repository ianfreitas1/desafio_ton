from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import WalletSerializer

from desafio_ton.cards.serializers import CardSerializer


class WalletView(APIView):

    def post(self, request):
        """Método POST para criar uma wallet."""

        data = request.data
        data['user'] = request.user.id

        serializer = WalletSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except:
                return Response(_('Failed to create wallet.'), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletDetailView(APIView):

    def get(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, id=wallet_id)

        serializer = WalletSerializer(wallet)

        return Response(serializer.data)

    def put(self, request, wallet_id):
        """Método PUT para alterar o limite de uma wallet."""

        wallet = get_object_or_404(Wallet, id=wallet_id)

        serializer = WalletSerializer(wallet, data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                return Response(_('Failed to edit card.'), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, wallet_id):
        """Método DELETE para deletar uma wallet."""

        wallet = get_object_or_404(Wallet, id=wallet_id)

        wallet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class WalletCardsView(APIView):

    def get(self, request, wallet_id):
        """Método GET para retornar todos os cartões de uma wallet."""

        wallet = get_object_or_404(Wallet, id=wallet_id)

        cards = wallet.cards.all()

        serializer = CardSerializer(cards, many=True)

        return Response({'cards': serializer.data})

    def post(self, request, wallet_id):
        """Método POST para adicionar um cartão à wallet."""

        wallet = get_object_or_404(Wallet, id=wallet_id)

        card_id = request.data['card_id']

        card = wallet.cards.get(id=card_id)

        card.wallet = wallet

        card.save()

        return Response(_('Added card to wallet.', status=status.HTTP_201_CREATED))

    def delete(self, request, walled_id):
        """Método DELETE para remover um cartão da wallet."""

        wallet = get_object_or_404(Wallet, id=walled_id)

        card_id = request.data['card_id']

        card = wallet.cards.get(id=card_id)

        card.wallet = None

        card.save()

        return Response(_('Removed card from wallet.', status=status.HTTP_200_OK))
