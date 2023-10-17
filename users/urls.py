from django.urls import include, path

from .views import LoginView

urlpatterns = [
    path("auth/token/login/", LoginView.as_view(), name="login"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
