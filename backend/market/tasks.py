from decimal import Decimal
import random

from celery import shared_task
from django.db import transaction

from .models import Asset, ArbitrageOpportunity, Exchange, PriceSnapshot


MOCK_EXCHANGES = ["AlphaEx", "BetaHub", "GammaMarkets"]
MOCK_ASSETS = [
    ("BTC-USD", "crypto", Decimal("68000.00")),
    ("ETH-USD", "crypto", Decimal("3600.00")),
    ("AAPL", "stock", Decimal("215.00")),
    ("MSFT", "stock", Decimal("430.00")),
    ("TSLA", "stock", Decimal("195.00")),
]


def _mock_price(base_price: Decimal) -> Decimal:
    variance = Decimal(str(random.uniform(-0.02, 0.02)))
    return (base_price * (Decimal("1.0") + variance)).quantize(Decimal("0.00000001"))


@shared_task
def poll_mock_exchanges():
    exchanges = []
    for name in MOCK_EXCHANGES:
        exchange, _ = Exchange.objects.get_or_create(
            name=name,
            defaults={"base_url": f"https://mock.{name.lower()}.example.com"},
        )
        exchanges.append(exchange)

    for symbol, asset_type, base_price in MOCK_ASSETS:
        asset, _ = Asset.objects.get_or_create(symbol=symbol, defaults={"asset_type": asset_type})
        snapshots = []

        for exchange in exchanges:
            price = _mock_price(base_price)
            snapshot = PriceSnapshot.objects.create(
                exchange=exchange,
                asset=asset,
                price=price,
            )
            snapshots.append(snapshot)

        cheapest = min(snapshots, key=lambda s: s.price)
        highest = max(snapshots, key=lambda s: s.price)

        spread_absolute = (highest.price - cheapest.price).quantize(Decimal("0.00000001"))
        spread_percent = (
            ((highest.price - cheapest.price) / cheapest.price) * Decimal("100")
        ).quantize(Decimal("0.0001"))

        with transaction.atomic():
            ArbitrageOpportunity.objects.update_or_create(
                asset=asset,
                defaults={
                    "cheapest_exchange": cheapest.exchange,
                    "most_expensive_exchange": highest.exchange,
                    "cheapest_price": cheapest.price,
                    "highest_price": highest.price,
                    "spread_absolute": spread_absolute,
                    "spread_percent": spread_percent,
                },
            )
