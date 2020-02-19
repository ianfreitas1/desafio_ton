from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    max_limit = serializers.SerializerMethodField()
    available_credit = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ('id', 'user', 'limit', 'max_limit', 'available_credit')

    def get_max_limit(self, obj):
        cards = obj.cards.all()

        max_limit = 0
        for card in cards:
            max_limit += card.limit

        return max_limit

    def get_available_credit(self, obj):
        cards = obj.cards.all()

        available_credit = 0
        for card in cards:
            available_credit += card.available_credit

        return available_credit
