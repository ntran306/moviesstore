from django.urls import path
from . import views

urlpatterns = [
    # movie likes
    path('movie/<int:movie_id>/like/',   views.like_movie,   name='likes.like_movie'),
    path('movie/<int:movie_id>/unlike/', views.unlike_movie, name='likes.unlike_movie'),

    # review (comment) likes
    path('review/<int:review_id>/like/',   views.like_review,   name='likes.like_review'),
    path('review/<int:review_id>/unlike/', views.unlike_review, name='likes.unlike_review'),
]
