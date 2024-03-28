from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", include("products.urls")),
    path("api/assets/", include("assets.urls")),
    path("api/about/", include("about.urls")),
]
