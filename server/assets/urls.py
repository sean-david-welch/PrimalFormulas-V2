from django.urls import path
from assets.views import AssetList, AssetDetail

urlpatterns = [
    path("assets", AssetList.as_view(), name="asset-list"),
    path("assets/<slug:name>", AssetDetail.as_view(), name="asset-detail"),
]
