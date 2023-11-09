from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    # Foreign key to the User model, representing the author or creator of the book.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books_created")
    
    # Character fields for the title and author of the book.
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    
    # Optional fields: ISBN number and cover image URL.
    isbn_number = models.CharField(max_length=13, null=True, blank=True)
    cover_image = models.URLField(null=True, blank=True)
    
    # Many-to-many relationship with the Category model through the intermediate model 'BookCategory'.
    categories = models.ManyToManyField(
        "Category",
        through='BookCategory',
        related_name="books"
    )
    
    # Date field for the publication date of the book. It can be null and left blank.
    publication_date = models.DateField(null=True, blank=True)
