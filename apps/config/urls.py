from django.urls import path

from apps.config import views

appname = "shortener"

urlpatterns = [
    path('', views.home, name='homepage'),
    path('my_links/', views.user_links, name='links'),
    path('<str:shortened_part>', views.redirect_url_view, name='redirect'),
    path('delete/<int:pk>', views.delete, name='delete'),
]