from django.urls import path
from .views import ArbitrageOpportunityListView, LatestSnapshotsView, average_spread_per_hour

urlpatterns = [
    path("opportunities/", ArbitrageOpportunityListView.as_view(), name="opportunities"),
    path("snapshots/", LatestSnapshotsView.as_view(), name="snapshots"),
    path(
        "analytics/average-spread-per-hour/",
        average_spread_per_hour,
        name="average-spread-per-hour",
    ),
]
