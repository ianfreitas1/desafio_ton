from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Card(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    card_number = models.CharField(
        verbose_name=_('card number'), max_length=16)
    due_date = models.DateField(verbose_name=_('due date'))
    expiration_date = models.DateField(verbose_name=_('expiration date'))
    user_name = models.CharField(verbose_name=_('user name'), max_length=100)
    cvv = models.CharField(max_length=4)
    limit = models.FloatField(verbose_name=_('limit'))
    # wallet = models.ForeignKey(Wallet, null=True, blank=True, default=None, related_name='cards')
