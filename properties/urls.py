from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='property_list'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('search/', views.PropertySearchView.as_view(), name='property_search'),
    path('cache-stats/', views.cache_stats_view, name='cache_stats'),
]