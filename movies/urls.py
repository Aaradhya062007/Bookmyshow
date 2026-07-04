from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),  # Pointing directly to the second view layout
    path('<int:movie_id>/theaters/', views.theater_list, name='theater_list'),
    path('theater/<int:theater_id>/book/', views.book_seats, name='book_seats'),
]