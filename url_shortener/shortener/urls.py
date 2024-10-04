from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_short_url, name='create_short_url'),
    path('urls/', views.url_list, name='url_list'),
]