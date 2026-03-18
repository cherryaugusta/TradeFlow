from django.contrib import admin
from .models import Exchange, Asset, PriceSnapshot, ArbitrageOpportunity

admin.site.register(Exchange)
admin.site.register(Asset)
admin.site.register(PriceSnapshot)
admin.site.register(ArbitrageOpportunity)
