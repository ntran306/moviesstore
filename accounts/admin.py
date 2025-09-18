from django.contrib import admin
from .models import UserSecurityPhrase   # ← update this import

@admin.register(UserSecurityPhrase)
class UserSecurityPhraseAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at")
    search_fields = ("user__username", "user__email")
