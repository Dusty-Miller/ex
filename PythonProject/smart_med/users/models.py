from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    preferences = models.JSONField(default=dict, blank=True)

class Protector(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='protectors')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    relation = models.CharField(max_length=30, blank=True)

