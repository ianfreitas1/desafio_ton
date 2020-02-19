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
        cards = Card.objects.filter(user=request.user)

        serializer = CardSerializer(cards, many=True)

        return Response({'cards': serializer.data})

    def post(self, request):
        data = request.data

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
        card = get_object_or_404(Card, id=card_id)

        serializer = CardSerializer(card)

        return Response(serializer.data)

    def put(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)

        serializer = CardSerializer(card, data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                return Response(_('Failed to edit card.'), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, card_id):
        card = get_object_or_404(Card, id=card_id)

        card.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
