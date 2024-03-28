from django.urls import path

from about.views import AboutList

urlpatterns = [
    path("about/", AboutList.as_view(), name="about-list"),
    path("about/<uuid:pk>/", AboutList.as_view(), name="about-detail"),
]
