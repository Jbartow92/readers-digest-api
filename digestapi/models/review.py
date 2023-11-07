from django.db import models
from django.contrib.auth.models import User
from .book import Book

 
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)