from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Card
from .serializers import CardSerializer


class CardView(APIView):

    def get(self, request):
        """Método GET para obter todos os cartões do usuário."""

        cards = Card.objects.filter(user=request.user)

        serializer = CardSerializer(cards, many=True)

        return Response({'cards': serializer.data})

    def post(self, request):
        """Método POST para criar um novo cartão."""

        data = request.data
        data['user'] = request.user.id

        serializer = CardSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except:
                return Response(_('Failed to add new card.'), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetailView(APIView):

    def get(self, request, card_id):
        """Método GET para obter os detalhes de um cartão."""

        card = get_object_or_404(Card, id=card_id)

        serializer = CardSerializer(card)

        return Response(serializer.data)

    def put(self, request, card_id):
        """Método PUT para editar os dados do cartão."""

        data = request.data

        card = get_object_or_404(Card, id=card_id)

        old_limit = card.limit
        new_limit = data['limit']

        if new_limit < old_limit:
            card.wallet.limit -= (old_limit - new_limit)
            card.wallet.save()

        data['user'] = request.user.id
        serializer = CardSerializer(card, data=data)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                return Response(_('Failed to edit card.'), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, card_id):
        """Método DELETE para deletar um cartão."""

        card = get_object_or_404(Card, id=card_id)

        if card.wallet is not None:
            card.wallet.limit -= card.limit
            card.wallet.save()

        card.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, card_id):
        """Método POST para pagar uma conta e liberar crédito."""

        card = get_object_or_404(Card, id=card_id)

        payment_value = request.data['payment_value']

        card.available_credit += payment_value

        card.save()

        serializer = CardSerializer(card)

        return Response({'detail': _('Paid bill and freed credit.'), 'card': serializer.data})
