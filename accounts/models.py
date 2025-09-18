from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

User = get_user_model()

class UserSecurityPhrase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_phrase')
    phrase_hash = models.CharField(max_length=128)
    updated_at = models.DateTimeField(default=timezone.now)

    def set_phrase(self, raw_phrase: str):
        self.phrase_hash = make_password((raw_phrase or "").strip())

    def check_phrase(self, raw_phrase: str) -> bool:
        return check_password((raw_phrase or "").strip(), self.phrase_hash)

    def __str__(self):
        return f"SecurityPhrase<{self.user}>"
