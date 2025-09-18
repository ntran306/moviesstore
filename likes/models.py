from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie, Review

# Stores likes that users give to a specific movie
class MovieLike(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='movie_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')
        indexes = [
            models.Index(fields=['movie', 'user'])
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.movie.name}"


# Stores likes that users give to a specific review (comment)
class ReviewLike(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')
        indexes = [
            models.Index(fields=['review', 'user'])
        ]

    def __str__(self):
        return f"{self.user.username} likes review {self.review.id}"
