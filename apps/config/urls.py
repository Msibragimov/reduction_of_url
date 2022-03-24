from django.urls import path

from apps.config.views import home, redirect_url_view

appname = "shortener"

urlpatterns = [
    path('', home, name='homepage'),
    path('<str:shortened_part>', redirect_url_view, name='redirect'),
]