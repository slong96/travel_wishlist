from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Views is where app logic goes.

# A - STEP 3/3: Returning the request from urls.py from travel_wishlist folder,
# this will render the html page
@login_required
def place_list(request):
    if request.method == 'POST':
        # create a new place
        form = NewPlaceForm(request.POST) # creating a form from data in the request
        place = form.save(commit=False) # creating a model object from form
        place.user = request.user
        if form.is_valid(): # validation againsts DB constraints
            place.save() # saves place to db
            return redirect('place_list') # reloads home page.
        
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
        
    # return redirect to wishlist places
    return redirect('place_list')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # Does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()

    # Is this a GET request (show data + form) or POST request (update Place object)?
    # If POST request, validate form data, and update
    if request.method == 'POST':
        # this means that we will make a new TripReviewForm object from the data...
        # that was sent with the HTTP request and we will put in data that the user...
        # has sent and use that to update.
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temporary, refine later
        return redirect('place_details', place_pk=place_pk)
    
    else:
        # If GET request, show Place info and optional form.
        # if place is visited, show form; if place is not visited, no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


@login_required
def about(request):
    author = 'Sophanda'
    about = 'A travel wishlist website, built with Django.'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})