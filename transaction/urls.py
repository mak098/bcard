from django.urls import include, path
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
router.register(r'transactions', views.CashInViewSet, basename ='transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('cashin/create/', views.CashInViewSet.as_view({'post': 'create'}), name='create'),
    path('cashin/get/<code>', views.CashInViewSet.as_view({'get': 'get'}), name='get'),
    # path('get-all/', views.InterrestRateConfigViewSet.as_view({'get': 'get_all_destination'}), name='get_all'),
]