import json
from django.core.management.base import BaseCommand
from alerts.models import SensorData

class Command(BaseCommand):
    help = "센서 상태 데이터를 JSON 파일로부터 불러오기"

    def handle(self, *args, **kwargs):
        with open('data/sensor_dataset.json', encoding='utf-8') as f:
            data = json.load(f)

            for entry in data:
                SensorData.objects.create(
                    is_opened=entry.get('isOpened', False),
                    sensor_value=entry.get('Sensor', 0),
                    heart_rate=entry.get('heart rate', None)
                )

        self.stdout.write(self.style.SUCCESS("✅ 센서 데이터 업로드 완료"))
