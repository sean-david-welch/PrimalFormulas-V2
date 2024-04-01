from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from primalformulas.views import (
    CatchAllView,
    HomeView,
    LoginView,
    LogoutView,
    RegisterView,
)

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/", include("assets.urls")),
    path("api/", include("about.urls")),
    path("api/", include("payments.urls")),
]

urlpatterns += [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]

urlpatterns += [
    path("", HomeView.as_view(), name="home"),
    path("<path:resource>", CatchAllView.as_view(), name="catch-all"),
]
