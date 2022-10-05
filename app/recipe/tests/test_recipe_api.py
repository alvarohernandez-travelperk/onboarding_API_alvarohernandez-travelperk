"""
Test for recipe APIs.
"""
# from venv import create
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Recipe, Ingredient,)

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)

import datetime
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return a recipe detail URL>"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


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

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe()

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = {
            'title': 'Sample recipe',
            'description': 'Sample description',
        }
        res = self.client.post(RECIPES_URL, payload)
        # Testing logger in python
        # logger.warning('Recipe created for testing at ' +
                    #    str(datetime.datetime.now())+' hours!')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_partial_update(self):
        """Test partial update of a recipe."""
        mockDescription = 'Sample recipe description'
        recipe = create_recipe(title='Sample recipe title',
                               description=mockDescription)

        payload = {'title': 'Sample recipe title updated'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.description, mockDescription)

    def test_full_update(self):
        """Test full update of a recipe."""
        mockTitle = 'Sample recipe title'
        mockDescription = 'Sample recipe description'
        recipe = create_recipe(title=mockTitle, description=mockDescription)

        payload = {'title': 'Sample recipe title updated',
                   'description': 'Sample recipe description updated'}
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        # self.assertEqual(recipe.title, payload['title'])
        # self.assertEqual(recipe.description, payload['description'])

    def test_delete_recipe(self):
        """Test deleting a recipe successful."""
        recipe = create_recipe()

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_ingredients(self):
        """Test creating a recipe with new ingredients."""
        payload = {
            'title': 'Salad',
            'description': 'Healthy Homemade Salad',
            'ingredients': [
                {'name': 'Tomato'},
                {'name': 'Olive Oil'},
                {'name': 'Arugula'},
            ],
        }
        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Fix to run the test but needs better solution, no need to filter
        recipes = Recipe.objects.filter()
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 3)
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                name=ingredient['name'],
            ).exists()
            self.assertTrue(exists)

    def test_create_ingredient_on_update(self):
        """Test creating an ingredient when updating a recipe."""
        recipe = create_recipe()

        payload = {'ingredients': [{'name': 'Limes'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_ingredient = Ingredient.objects.get(name='Limes')
        self.assertIn(new_ingredient, recipe.ingredients.all())

    def test_update_recipe_assign_ingredient(self):
        """Test assigning an existing ingredient when updating a recipe."""
        ingredient1 = Ingredient.objects.create(name='Pepper')
        recipe = create_recipe()
        recipe.ingredients.add(ingredient1)

        ingredient2 = Ingredient.objects.create(name='Chili')
        payload = {'ingredients': [{'name': 'Chili'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(ingredient2, recipe.ingredients.all())
        self.assertNotIn(ingredient1, recipe.ingredients.all())

    def test_clear_recipe_ingredients(self):
        """Test clearing a recipes ingredients."""
        ingredient = Ingredient.objects.create(name='Garlic')
        recipe = create_recipe()
        recipe.ingredients.add(ingredient)

        payload = {'ingredients': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)
