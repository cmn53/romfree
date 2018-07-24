from django.urls import path
from . import views

app_name = 'rom'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/<metro_code>/<arrival_id>/', views.results, name='results'),
    path('hotel/<int:hotel_id>/', views.detail, name='detail'),
]
