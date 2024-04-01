from django.urls import path

from about.views import AboutDetail, AboutList

urlpatterns = [
    path("about", AboutList.as_view(), name="about-list"),
    path("about/<uuid:pk>", AboutDetail.as_view(), name="about-detail"),
]
