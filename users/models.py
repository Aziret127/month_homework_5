import random
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code', null=True)
    code = models.CharField(max_length=6, default='000000')
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code = f"{random.randint(100000, 999999)}"
        self.save()

    def __str__(self):
        return f"Confirmation code for {self.user.username}"