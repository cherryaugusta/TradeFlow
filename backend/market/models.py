from django.db import models


class Exchange(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    asset_type = models.CharField(
        max_length=20,
        choices=[("crypto", "crypto"), ("stock", "stock")],
    )

    def __str__(self):
        return self.symbol


class PriceSnapshot(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name="snapshots")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="snapshots")
    price = models.DecimalField(max_digits=20, decimal_places=8)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["asset", "recorded_at"]),
            models.Index(fields=["exchange", "recorded_at"]),
        ]
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.exchange.name} {self.asset.symbol} {self.price}"


class ArbitrageOpportunity(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="opportunities")
    cheapest_exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name="cheap_opportunities",
    )
    most_expensive_exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name="expensive_opportunities",
    )
    cheapest_price = models.DecimalField(max_digits=20, decimal_places=8)
    highest_price = models.DecimalField(max_digits=20, decimal_places=8)
    spread_absolute = models.DecimalField(max_digits=20, decimal_places=8)
    spread_percent = models.DecimalField(max_digits=10, decimal_places=4)
    observed_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["asset", "observed_at"]),
        ]
        ordering = ["-spread_percent", "-observed_at"]

    def __str__(self):
        return f"{self.asset.symbol} {self.spread_percent}%"
