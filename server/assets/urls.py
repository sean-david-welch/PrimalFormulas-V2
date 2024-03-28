from django.urls import path
from assets.views import AssetsList, AssetDetail

urlpatterns = [
    path("assets/", AssetsList.as_view(), name="asset-list"),
    path("assets/<slug:name>/", AssetDetail.as_view(), name="asset-detail"),
]
