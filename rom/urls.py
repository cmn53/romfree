from django.urls import path
from . import views

app_name = 'rom'
urlpatterns = [
    path('', views.index, name='index'),
    path('<metro_id>/<arrival_id>/results/', views.results, name='results'),
    path('hotel/<int:hotel_id>/', views.detail, name='detail'),
]
