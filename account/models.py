from django.db import models
from django.conf import settings


class Profile(models.Model):
    SATATUS_CHOICES = (
        ("m", "Man"),
        ("w", "Woman"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    gender = models.CharField(max_length=1, choices=SATATUS_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    credit = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile for user { self.user.username }"
