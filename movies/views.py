# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Movie, Theater, Seat, Booking

def movie_list(request):
    search_query = request.GET.get('search')
    movies = Movie.objects.all()
    if search_query:
        movies = movies.filter(name__icontains=search_query)
    return render(request, 'movies/movie_list.html', {'movies': movies})

def theater_list(request, movie_id):
    # Using select_related to optimize database queries
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie).select_related('movie')
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    
    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')
        
        if not selected_seat_ids:
            return render(request, "movies/seat_selection.html", {
                'theater': theater,
                'seats': Seat.objects.filter(theater=theater),
                'error': "No seats selected."
            })
        
        # Transaction ensures data consistency
        with transaction.atomic():
            # select_for_update() locks the selected rows until the transaction finishes
            seats = Seat.objects.select_for_update().filter(
                id__in=selected_seat_ids, 
                theater=theater
            )
            
            error_seats = []
            for seat in seats:
                if seat.is_booked:
                    error_seats.append(seat.seat_number)
                else:
                    Booking.objects.create(
                        user=request.user,
                        seat=seat,
                        movie=theater.movie,
                        theater=theater
                    )
                    seat.is_booked = True
                    seat.save()
            
            if error_seats:
                return render(request, 'movies/seat_selection.html', {
                    'theater': theater,
                    'seats': Seat.objects.filter(theater=theater),
                    'error': f"Seats already taken: {', '.join(error_seats)}"
                })
        
        return redirect('profile')
            
    seats = Seat.objects.filter(theater=theater)
    return render(request, 'movies/seat_selection.html', {'theater': theater, 'seats': seats})