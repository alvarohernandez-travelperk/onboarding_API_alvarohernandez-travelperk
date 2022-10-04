"""
Tests for ingredients API.
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')

def detail_url(ingredient_id):
    """create and return an Ingredient detail URL"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class PrivateIngredientsApiTests(TestCase):
    """Test API requests."""

    def setUp(self):
        self.client = APIClient()
    
    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(name='Kale')
        Ingredient.objects.create(name='Vanilla')
        
        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_ingredient(self):
        """Test updating ingredients"""
        ingredient = Ingredient.objects.create(name='Cilantro')

        payload = {'name': 'Coriander'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])


    def test_delete_ingredient(self):
        """Test deleting an ingredient"""
        ingredient = Ingredient.objects.create(name='Lettuce')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects
        self.assertFalse(ingredients.exists())
