from django.urls import path
from .views import home
from .views import create_password

urlpatterns = [
    path("", home, name="home"),
    path("", create_password, name="create_password")
]