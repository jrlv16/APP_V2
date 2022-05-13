from django.urls import path, include
from rest_framework.routers import DefaultRouter

from client import views

router = DefaultRouter()
router.register('cat', views.CatViewSet)
router.register('telephone', views.TelephoneViewSet)

app_name = 'client/'

urlpatterns = [
    path('', include(router.urls))
]
