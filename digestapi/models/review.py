from django.db import models
from django.contrib.auth.models import User
from .book import Book

class Review(models.Model):
    # Foreign key to the Book model, establishing a relationship between Book and Review.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    # Foreign key to the User model, establishing a relationship between User and Review.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Integer field for rating with choices from 1 to 10.
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    
    # TextField for comments.
    comment = models.TextField()
    
    # DateTimeField for the date the review was posted, automatically set to the current date and time.
    date_posted = models.DateTimeField(auto_now_add=True)
