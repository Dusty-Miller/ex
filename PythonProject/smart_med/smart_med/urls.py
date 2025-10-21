from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from medications.views import MedicationViewSet, MedicationScheduleViewSet, MedicationHistoryViewSet

router = DefaultRouter()
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'schedules', MedicationScheduleViewSet, basename='schedule')
router.register(r'history', MedicationHistoryViewSet, basename='history')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/alerts/', include('alerts.urls')),
    path('api/qna/', include('qna.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 공통 API 라우터
    path('api/', include(router.urls)),
]
