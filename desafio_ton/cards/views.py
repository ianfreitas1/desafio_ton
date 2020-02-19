from django.shortcuts import get_object_or_404
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

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        serializer = CardSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response("erro ao criar cartão", status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
