from django.urls import include, path
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
router.register(r'interestConfigs', views.InterrestRateConfigViewSet, basename ='interestConfig')

urlpatterns = [
    path('', include(router.urls)),
    path('get-destination/', views.InterrestRateConfigViewSet.as_view({'get': 'get_destination'}), name='get'),
    path('get-all-destination/', views.InterrestRateConfigViewSet.as_view({'get': 'get_all_destination'}), name='get_all'),
]