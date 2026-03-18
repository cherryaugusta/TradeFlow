from rest_framework import serializers
from .models import ArbitrageOpportunity, PriceSnapshot


class PriceSnapshotSerializer(serializers.ModelSerializer):
    exchange_name = serializers.CharField(source="exchange.name", read_only=True)
    asset_symbol = serializers.CharField(source="asset.symbol", read_only=True)

    class Meta:
        model = PriceSnapshot
        fields = [
            "id",
            "exchange",
            "exchange_name",
            "asset",
            "asset_symbol",
            "price",
            "recorded_at",
        ]


class ArbitrageOpportunitySerializer(serializers.ModelSerializer):
    asset_symbol = serializers.CharField(source="asset.symbol", read_only=True)
    cheapest_exchange_name = serializers.CharField(source="cheapest_exchange.name", read_only=True)
    most_expensive_exchange_name = serializers.CharField(source="most_expensive_exchange.name", read_only=True)

    class Meta:
        model = ArbitrageOpportunity
        fields = [
            "id",
            "asset_symbol",
            "cheapest_exchange_name",
            "most_expensive_exchange_name",
            "cheapest_price",
            "highest_price",
            "spread_absolute",
            "spread_percent",
            "observed_at",
        ]
