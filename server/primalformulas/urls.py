from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from views import LoginView, RegisterView

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/", include("assets.urls")),
    path("api/", include("about.urls")),
]

urlpatterns += [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
]
