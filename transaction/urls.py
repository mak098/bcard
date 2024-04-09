from django.urls import include, path
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
router.register(r'cashins', views.CashInViewSet, basename ='cashin')
router.register(r'cashouts', views.cashOutViewSet, basename ='cashout')

urlpatterns = [
    path('', include(router.urls)),
    path('cashin/create/', views.CashInViewSet.as_view({'post': 'create'}), name='create'),
    path('cashin/get/<str:code>/', views.CashInViewSet.as_view({'get': 'get_with_code'}), name='get_with_code'),
    path('cashout/create/', views.cashOutViewSet.as_view({'post': 'out'}), name='out'),
    path('cashout/statement/<str:code>/', views.cashOutViewSet.as_view({'get': 'statement'}), name='out'),
]