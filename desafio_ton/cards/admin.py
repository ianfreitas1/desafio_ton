from django.contrib import admin
from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'limit', 'wallet')
    search_fields = ('user', 'wallet')
    list_filter = ('user', 'wallet')


admin.site.register(Card, CardAdmin)
