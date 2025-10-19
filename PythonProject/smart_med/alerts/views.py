# alerts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from medications.models import Medication
from django.utils import timezone

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sensor_payload(request):
    """
    IoT에서 전송된 센서 데이터 처리 API
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

        # 실제 로직: 무게 변화를 기반으로 복용 여부 판단
        # 예: 0.3g 이상 줄어들면 ‘복용됨’으로 표시
        if weight < 0.3:
            status_msg = "복용 안 됨 (미복용)"
        else:
            status_msg = "복용됨 ✅"

        # DB 업데이트 예시
        med = Medication.objects.get(id=med_id, user_id=user_id)
        med.last_checked = timezone.now()
        med.save()

        return Response({
            "message": "센서 데이터 수신 완료",
            "user_id": user_id,
            "medication_id": med_id,
            "weight": weight,
            "status": status_msg
        }, status=status.HTTP_200_OK)

    except Medication.DoesNotExist:
        return Response({"error": "해당 약 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
