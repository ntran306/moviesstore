from django.contrib import admin
from .models import Movie, Review, MoviePetition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)

@admin.register(MoviePetition)
class MoviePetitionAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'creator', 'yes_votes', 'no_votes', 'approval_percentage', 'created_at']
    list_filter = ['created_at']
    search_fields = ['movie_title', 'description', 'creator__username']
    readonly_fields = ['created_at', 'yes_votes', 'no_votes']

    def approval_percentage(self, obj):
        return f"{obj.approval_percentage}%"
    approval_percentage.short_description = "Approval %"

@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition', 'vote_type', 'voted_at']
    list_filter = ['vote_type', 'voted_at']
    search_fields = ['user__username', 'petition__movie_title']