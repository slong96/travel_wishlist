from django.urls import path
from . import views 

# A - STEP 2/3: Received request from urls.py from wishlist folder,
# if there is no path, it displays place_list function
# from views.py
urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('visited', views.places_visited, name='places_visited'),
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    path('about', views.about, name='about'),
]