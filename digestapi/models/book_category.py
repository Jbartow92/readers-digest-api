from django.db import models
from .book import Book
from .category import Category

class BookCategory(models.Model):
    # Foreign key to the Book model, establishing a relationship between Book and BookCategory.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    # Foreign key to the Category model, establishing a relationship between Category and BookCategory.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
