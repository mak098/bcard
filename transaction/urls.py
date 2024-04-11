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

    path('cashin/today/', views.CashInViewSet.as_view({'get': 'today'}), name='today'),
    path('cashin/week/', views.CashInViewSet.as_view({'get': 'week'}), name='week'),
    path('cashin/month/', views.CashInViewSet.as_view({'get': 'month'}), name='month'),
    path('cashin/year/', views.CashInViewSet.as_view({'get': 'year'}), name='year'),
    path('cashin/customer-date/<str:start_date>/<str:end_date>/', views.CashInViewSet.as_view({'get': 'personalized_date'}), name='year'),

    path('cashout/create/', views.cashOutViewSet.as_view({'post': 'out'}), name='out'),
    path('cashout/statement/<str:code>/', views.cashOutViewSet.as_view({'get': 'statement'}), name='out'),
    path('cashout/today/', views.cashOutViewSet.as_view({'get': 'today'}), name='today'),
    path('cashout/week/', views.cashOutViewSet.as_view({'get': 'week'}), name='week'),
    path('cashout/month/', views.cashOutViewSet.as_view({'get': 'month'}), name='month'),
    path('cashout/year/', views.cashOutViewSet.as_view({'get': 'year'}), name='year'),
]