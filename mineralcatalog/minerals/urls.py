from django.urls import path

from . import views


app_name = 'minerals'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:mineral_id>/', views.detail, name='detail'),
    path('random_mineral/', views.random_mineral, name='random_mineral')
]