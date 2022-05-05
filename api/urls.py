from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApiIndexViewSet

router = DefaultRouter()
router.register(r'', ApiIndexViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
