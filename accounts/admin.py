from django.contrib import admin
from .models import SecurityQuestion, UserSecurityAnswer

@admin.register(SecurityQuestion)
class SecurityQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
    search_fields = ("text",)

@admin.register(UserSecurityAnswer)
class UserSecurityAnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "updated_at")
    search_fields = ("user__username", "question__text")
