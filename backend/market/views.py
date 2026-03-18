from django.db.models import Avg
from django.db.models.functions import TruncHour
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ArbitrageOpportunity, PriceSnapshot
from .serializers import ArbitrageOpportunitySerializer, PriceSnapshotSerializer


class ArbitrageOpportunityListView(APIView):
    def get(self, request):
        queryset = ArbitrageOpportunity.objects.select_related(
            "asset", "cheapest_exchange", "most_expensive_exchange"
        ).all()[:500]
        serializer = ArbitrageOpportunitySerializer(queryset, many=True)
        return Response(serializer.data)


class LatestSnapshotsView(APIView):
    def get(self, request):
        queryset = PriceSnapshot.objects.select_related("exchange", "asset").all()[:500]
        serializer = PriceSnapshotSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def average_spread_per_hour(request):
    queryset = (
        ArbitrageOpportunity.objects.annotate(hour=TruncHour("observed_at"))
        .values("hour", "asset__symbol")
        .annotate(avg_spread_percent=Avg("spread_percent"))
        .order_by("-hour", "asset__symbol")
    )
    return Response(list(queryset))
