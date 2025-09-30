from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.comment

class MoviePetition(models.Model):
    movie_title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Petition: {self.movie_title}"
    
    @property
    def total_votes(self):
        return self.yes_votes + self.no_votes
    
    @property
    def approval_percentage(self):
        if self.total_votes == 0:
            return 0
        return round((self.yes_votes / self.total_votes * 100, 1))

class PetitionVote(models.Model):
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.BooleanField()
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')

    def __str__(self):
        vote = "Yes" if self.vote_type else "No"
        return f"{self.user.username} voted {vote} on {self.petition.movie_title}"