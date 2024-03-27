from django.contrib import admin

from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", include("products.urls")),
    path("api/assets/", include("assets.urls")),
    path("api/about/", include("about.urls")),
]
