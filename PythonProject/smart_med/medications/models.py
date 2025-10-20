from django.db import models
from users.models import User

class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=200)
    dose = models.CharField(max_length=50)
    times_per_day = models.IntegerField(default=1)
    intake_timing = models.CharField(max_length=20, blank=True)  # 식전/식후 등
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.name})"

class MedicationSchedule(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='schedules')
    scheduled_time = models.DateTimeField()

class MedicationHistory(models.Model):
    medication = models.ForeignKey('Medication', on_delete=models.CASCADE, related_name='histories')
    taken_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('taken','복용'),('missed','미복용')])

class MedicationInfo(models.Model):
    item_seq = models.CharField(max_length=50, unique=True)  # 품목번호
    name = models.CharField(max_length=255)  # 약 이름
    manufacturer = models.CharField(max_length=255, null=True, blank=True)  # 제조사
    efficacy = models.TextField(null=True, blank=True)  # 효능
    usage = models.TextField(null=True, blank=True)  # 사용법
    caution = models.TextField(null=True, blank=True)  # 주의사항
    contraindication = models.TextField(null=True, blank=True)  # 금기사항
    interaction = models.TextField(null=True, blank=True)  # 상호작용
    side_effect = models.TextField(null=True, blank=True)  # 부작용
    storage = models.TextField(null=True, blank=True)  # 보관방법
    image_url = models.URLField(null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    update_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
