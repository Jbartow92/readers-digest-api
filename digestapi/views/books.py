from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from digestapi.models import Book
from .categories import CategorySerializer

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    # Custom field to check if the authenticated user is the owner of the book
    is_owner = serializers.SerializerMethodField()
    
    # Nested serializer for the categories associated with the book
    categories = CategorySerializer(many=True)

    # Method to get the 'is_owner' field value
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user

    class Meta:
        model = Book
        # Fields to include in the serialized representation of the Book model
        fields = ['id', 'title', 'author', 'isbn_number', 'cover_image', 'is_owner', 'categories']

# ViewSet for handling Book-related operations
class BookViewSet(viewsets.ViewSet):

    # List all books
    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)

    # Retrieve a specific book by ID
    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Create a new book
    def create(self, request):
        # Get data from the client's JSON payload
        title = request.data.get('title')
        author = request.data.get('author')
        isbn_number = request.data.get('isbn_number')
        cover_image = request.data.get('cover_image')

        # Create a book database row
        book = Book.objects.create(
            user=request.user,
            title=title,
            author=author,
            cover_image=cover_image,
            isbn_number=isbn_number)

        # Establish many-to-many relationships for categories
        category_ids = request.data.get('categories', [])
        book.categories.set(category_ids)

        serializer = BookSerializer(book, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Update an existing book
    def update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)

            # Check if the authenticated user is allowed to edit this book
            self.check_object_permissions(request, book)

            # Validate and update book data
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                book.title = serializer.validated_data['title']
                book.author = serializer.validated_data['author']
                book.isbn_number = serializer.validated_data['isbn_number']
                book.cover_image = serializer.validated_data['cover_image']
                book.save()

                # Update many-to-many relationships for categories
                category_ids = request.data.get('categories', [])
                book.categories.set(category_ids)

                serializer = BookSerializer(book, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Delete an existing book
    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            # Check if the authenticated user is allowed to delete this book
            self.check_object_permissions(request, book)
            book.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
