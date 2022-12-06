"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)

from core.models import (
    Recipe,
    Ingredient,
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save()


class IngredientViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Manage ingredients in the database."""
    serializer_class = serializers. IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        """return queryset"""
        return self.queryset.order_by('-name')
