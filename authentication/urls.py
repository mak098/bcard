from django.urls import include, path
from rest_framework import routers

from . import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSets, basename ='user')

urlpatterns = [
    path('', include(router.urls)),
    path('signin/', views.UserViewSets.as_view({'post': 'signin'}), name='signin'),
    path('logout/', views.UserViewSets.as_view({'post': 'logout'}), name='logout'),

  ]