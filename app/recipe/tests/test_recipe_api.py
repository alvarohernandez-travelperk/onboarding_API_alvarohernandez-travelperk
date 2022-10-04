"""
Test for recipe APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(**params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'description': 'Sample description',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(**defaults)
    return recipe


class PrivateRecipeAPITests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving a couple of recipes"""
        create_recipe()
        create_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
