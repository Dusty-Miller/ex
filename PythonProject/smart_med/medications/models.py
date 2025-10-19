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
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='histories')
    taken_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(('taken','복용'),('missed','미복용'),('over','과복용')))

