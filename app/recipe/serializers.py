"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (Recipe, Ingredient,)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients']
        read_only_fields = ['id']

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Getting or creating ingredients as needed."""
        for ingredient in ingredients: 
            ingredient_obj, create = Ingredient.objects.get_or_create(**ingredient)
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe"""
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_ingredients(ingredients, recipe)
        
        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        ingredients = validated_data.pop('ingredients', None)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view. -  Extends RecipeSerializer class"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields
