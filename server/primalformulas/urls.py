from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/", include("assets.urls")),
    path("api/", include("about.urls")),
]
