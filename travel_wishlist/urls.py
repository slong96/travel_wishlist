from django.urls import path
from . import views 

# A - STEP 2/3: Received request from urls.py from wishlist folder,
# if there is no path, it displays place_list function
# from views.py
urlpatterns = [
    # path to homepage, this represents a request to the homepage
    path('', views.place_list, name='place_list'),
    # path to visited page, this represents a request to the visited page
    path('visited', views.places_visited, name='places_visited'),
    # path to place/?int? was visited, this has a int place holder
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    path('place/<int:place_pk>', views.place_details, name='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),
    # path to about page, this represents a request to the about page
    path('about', views.about, name='about'),
]