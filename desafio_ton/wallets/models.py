from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    limit = models.FloatField(verbose_name=_('limit'), default=0.0)

    class Meta:
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')

    def __str__(self):
        return "{0}'s wallet".format(self.user)
