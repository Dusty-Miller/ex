from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from medications.models import Medication
from medications.services import process_sensor
from .fcm_service import send_fcm_notification
from users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sensor_payload(request):
    """
    IoT에서 전송된 센서 데이터 처리 API + 보호자 알림 전송
    예시 body:
    {
      "user_id": 1,
      "medication_id": 5,
      "weight": 0.35
    }
    """
    try:
        data = request.data
        user_id = data.get("user_id")
        med_id = data.get("medication_id")
        weight = float(data.get("weight", 0))

        # 복용 상태 판별 및 DB 반영
        result = process_sensor(user_id, med_id, weight)

        # 약 정보 업데이트 (마지막 체크 시간 기록)
        med = Medication.objects.get(id=med_id, user_id=user_id)
        med.last_checked = timezone.now()
        med.save()

        # 보호자에게 FCM 푸시 전송
        user = User.objects.get(id=user_id)
        protector = user.protectors.first()  # 보호자 1명만 예시로 전송
        if protector and getattr(protector, "fcm_token", None):
            send_fcm_notification(
                token=protector.fcm_token,
                title="복약 알림",
                body=result.get("message", "복용 상태 업데이트")
            )

        return Response({
            "message": "센서 데이터 처리 및 알림 전송 완료",
            "user_id": user_id,
            "medication_id": med_id,
            "weight": weight,
            "status": result.get("status")
        }, status=status.HTTP_200_OK)

    except Medication.DoesNotExist:
        return Response(
            {"error": "해당 약 정보를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
