from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Models is where the database goes.

# Database / Model
class Place(models.Model):
    # Foreign key is built into Django models.
    # Name other table using a string, so for this, it's auth.User.
    # User can't be null.
    # if user is deleted, models.CASCADE will delete all their associated places.
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    # charfield has 200 character limit
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    # text field - you can have as much text as you want
    # notes can be null
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # if thers an old place, we will find preview version FIRST
        old_place = Place.objects.filter(pk=self.pk).first()
        # if old place and if old place has photo
        if old_place and old_place.photo:
            # and if that old place photo is not the same as new place object photo
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        # then call to super class method save.
        # this is defined by django.
        super().save(*args, **kwargs)

    
    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*args, **kwargs)


    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        note_str = self.notes[100:] if self.notes else 'no notes'
        return f'{self.name} visited? {self.visited} on {self.date_visited}. Notes: {note_str}. Photo {photo_str}'
