from django.db import models
from users.models import User

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=255, null=True, blank=True)


