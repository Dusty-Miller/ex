from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from medications.urls import router as meds_router

router = DefaultRouter()
router.registry.extend(meds_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/alerts/', include('alerts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/qna/', include('qna.urls')),
]
