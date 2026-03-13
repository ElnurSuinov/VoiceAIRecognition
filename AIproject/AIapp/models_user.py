from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLES = [
        ("client", "Client"),
        ("manager", "Manager"),
        ("risk", "Risk Officer"),
        ("admin", "Administrator"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default="client")

    def __str__(self):
        return f"{self.user.username} - {self.role}"