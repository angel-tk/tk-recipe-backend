from rest_framework.viewsets import ModelViewSet
from core.models import Recipe
from recipe import serializers

class RecipeViewSet(ModelViewSet):
    """Manage recipes in database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_serializer_class(self):
        """Return serializer class"""
        return self.serializer_class

    def get_queryset(self):
        """Retrieve recipes"""
        queryset = Recipe.objects.all()
        names = self.request.query_params.get('name')
        if names:
            queryset = queryset.filter(name__icontains=names)
        return queryset

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save()