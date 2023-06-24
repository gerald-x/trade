from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email])
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    initial_deposit = models.FloatField(default=100)
    is_admin = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["password", "email"]

class Records(models.Model):
    initial_value = models.FloatField(null=False, blank=False)
    profit_loss = models.FloatField(null=False, blank=False, default=0)
    current_value = models.FloatField(null=False, blank=False)
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records")