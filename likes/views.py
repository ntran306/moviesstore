from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie, Review
from .models import MovieLike, ReviewLike

@login_required
@require_POST
def like_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    MovieLike.objects.get_or_create(movie=movie, user=request.user)
    return redirect(request.META.get('HTTP_REFERER') or '/')

@login_required
@require_POST
def unlike_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    MovieLike.objects.filter(movie=movie, user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER') or '/')

@login_required
@require_POST
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ReviewLike.objects.get_or_create(review=review, user=request.user)
    return redirect(request.META.get('HTTP_REFERER') or '/')

@login_required
@require_POST
def unlike_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    ReviewLike.objects.filter(review=review, user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER') or '/')
