from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.shortcuts import render
from likes.models import ReviewLike

def top_comments(request):
    qs = (Review.objects
          .select_related('user', 'movie')
          .order_by('-date'))
    paginator = Paginator(qs, 10)  # Show 10 comments per page
    page_obj = paginator.get_page(request.GET.get('page'))
    template_data = {
        'title': 'Top Comments',
        'page_obj': page_obj,
    }
    return render(request, 'movies/top_comments.html', {'template_data': template_data})


def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=movie.id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
                      {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, 
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

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