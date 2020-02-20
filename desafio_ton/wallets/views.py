from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .permissions import WalletPermission
from .serializers import WalletSerializer

from desafio_ton.cards.models import Card
from desafio_ton.cards.serializers import CardSerializer


class WalletView(APIView):

    def post(self, request):
        """Método POST para criar uma wallet."""
        if Wallet.objects.filter(user=self.request.user).exists():
            return Response({'detail': _('User already has a wallet.')}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['user'] = request.user.id

        serializer = WalletSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except:
                return Response({'detail': _('Failed to create wallet.')}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletDetailView(APIView):
    permission_classes = [IsAuthenticated & WalletPermission]

    def get_object(self, wallet_id):
        wallet = get_object_or_404(Wallet, id=wallet_id)
        self.check_object_permissions(self.request, wallet)
        return wallet

    def get(self, request, wallet_id):
        """Método GET para obter detalhes de uma wallet."""
        wallet = self.get_object(wallet_id)

        serializer = WalletSerializer(wallet)

        return Response(serializer.data)

    def patch(self, request, wallet_id):
        """Método PATCH para alterar o limite de uma wallet."""
        limit = request.data['limit']

        wallet = self.get_object(wallet_id)

        serializer = WalletSerializer(wallet)

        max_limit = serializer.data['max_limit']

        if limit > max_limit:
            return Response({'detail': _('Requested limit is over maximum permitted.')},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = WalletSerializer(
            wallet, data={'limit': limit}, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                return Response({'detail': _('Failed to edit card.')}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, wallet_id):
        """Método DELETE para deletar uma wallet."""

        wallet = self.get_object(wallet_id)

        wallet_cards = wallet.cards.all()

        for card in wallet_cards:
            card.wallet = None
            card.save()

        wallet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, wallet_id):
        """Método POST para efetuar uma compra com a wallet."""

        wallet = self.get_object(wallet_id)

        wallet_cards = wallet.cards.all().order_by('-due_date', 'limit')

        order_value = request.data['order_value']

        card_credits = [card.available_credit for card in wallet_cards]
        credit_sum = sum(card_credits)

        if credit_sum < order_value:
            return Response({'detail': _('No credit available to pay order.')}, status=status.HTTP_400_BAD_REQUEST)

        # Essa lista irá conter os cartões utilizados na compra, marcados por uma
        # dicionário contendo o cartão e o valor pago por esse cartão
        cards_used = []

        index = 0
        while order_value > 0:
            card = wallet_cards[index]

            if card.available_credit > 0:

                if card.available_credit >= order_value:
                    paid_value = order_value
                    card.available_credit -= order_value
                    card.save()

                    serializer = CardSerializer(card)

                    cards_used.append(
                        {'card': serializer.data, 'paid_value': paid_value})

                    order_value = 0

                else:
                    order_value -= card.available_credit
                    paid_value = card.available_credit
                    card.available_credit = 0
                    card.save()

                    serializer = CardSerializer(card)

                    cards_used.append(
                        {'card': serializer.data, 'paid_value': paid_value})

            index += 1

        return Response({'cards_used': cards_used}, status=status.HTTP_200_OK)


class WalletCardsView(APIView):
    permission_classes = [IsAuthenticated & WalletPermission]

    def get_object(self, wallet_id):
        wallet = get_object_or_404(Wallet, id=wallet_id)
        self.check_object_permissions(self.request, wallet)
        return wallet

    def get(self, request, wallet_id):
        """Método GET para retornar todos os cartões de uma wallet."""

        wallet = self.get_object(wallet_id)

        cards = wallet.cards.all()

        serializer = CardSerializer(cards, many=True)

        return Response({'cards': serializer.data})

    def post(self, request, wallet_id):
        """Método POST para adicionar um cartão à wallet."""

        wallet = self.get_object(wallet_id)

        card_id = request.data['card_id']

        card = Card.objects.get(id=card_id)

        card.wallet = wallet

        card.save()

        return Response({'detail': _('Added card to wallet.')}, status=status.HTTP_201_CREATED)

    def delete(self, request, wallet_id):
        """Método DELETE para remover um cartão da wallet."""

        wallet = self.get_object(wallet_id)

        card_id = request.data['card_id']

        card = Card.objects.get(id=card_id)

        card.wallet = None

        card.save()

        serializer = WalletSerializer(wallet)

        max_limit = serializer.data['max_limit']

        if wallet.limit > max_limit:
            wallet.limit = max_limit
            wallet.save()

        return Response({'detail': _('Removed card from wallet.')}, status=status.HTTP_200_OK)
