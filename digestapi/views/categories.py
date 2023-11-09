from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from digestapi.models import Category

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # Fields to include in the serialized representation of the Category model
        fields = ['id', 'name']

# ViewSet for handling Category-related operations
class CategoryViewSet(viewsets.ViewSet):

    # Custom action to list all categories
    def list(self, request):
        # Retrieve all categories from the database
        categories = Category.objects.all()
        # Serialize the categories
        serializer = CategorySerializer(categories, many=True)
        # Return the serialized data in the response
        return Response(serializer.data)

    # Custom action to retrieve a specific category by its primary key (pk)
    def retrieve(self, request, pk=None):
        try:
            # Attempt to retrieve a category with the given primary key
            category = Category.objects.get(pk=pk)
            # Serialize the retrieved category
            serializer = CategorySerializer(category)
            # Return the serialized data in the response
            return Response(serializer.data)
        except Category.DoesNotExist:
            # Return a 404 response if the category is not found
            return Response(status=status.HTTP_404_NOT_FOUND)
