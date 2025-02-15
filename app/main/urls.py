# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermitViewSet, VerifyPermitView  #, ActivityLogViewSet

router = DefaultRouter()
router.register(r'permits', PermitViewSet, basename='permit')

# router.register(r'activity-logs', ActivityLogViewSet, basename='activity-log')

urlpatterns = [
    path('', include(router.urls)),
    path('verify/', VerifyPermitView.as_view(), name='verify-permit'),
]
