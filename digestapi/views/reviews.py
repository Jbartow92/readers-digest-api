from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from digestapi.models import Review, Book

class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'book_id', 'user_id', 'rating', 'comment', 'date_posted', 'is_owner']
        read_only_fields = ['user']

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review
        return self.context['request'].user == obj.user


class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        # Get all reviews
        reviews = Review.objects.all()
        # Serialize the objects, and pass request to determine owner
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})

        # Return the serialized data with 200 status code
        return Response(serializer.data)

    def create(self, request):
    # Validate input data
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Valid data, proceed to create the review
            book_id = request.data.get('book_id')
            rating = request.data.get('rating')
            comment = request.data.get('comment')
            date_posted = request.data.get('date_posted')

            # Ensure the book exists (you should handle potential exceptions here)
            try:
                book = Book.objects.get(pk=book_id)
            except Book.DoesNotExist:
                return Response({"error": "Invalid book_id"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the review
            review = Review.objects.create(
                book=book,
                user=request.user,
                rating=rating,
                comment=comment,
                date_posted=date_posted)

            # Serialize the newly created review
            serialized_review = ReviewSerializer(review, context={'request': request})

            # Return a response with the created review and a 201 status code
            return Response(serialized_review.data, status=status.HTTP_201_CREATED)

        # Invalid data; return a 400 Bad Request response with validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            # Get the requested review
            review = Review.objects.get(pk=pk)
            # Serialize the object (make sure to pass the request as context)
            serializer = ReviewSerializer(review, context={'request': request})
            # Return the review with 200 status code
            return Response(serializer.data)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            # Get the requested review
            review = Review.objects.get(pk=pk)

            # Check if the user has permission to delete
            # Will return 403 if authenticated user is not author
            if review.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Delete the review
            review.delete()

            # Return success but no body
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)