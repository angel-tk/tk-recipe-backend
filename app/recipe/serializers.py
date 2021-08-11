from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializers for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializers for recipe object"""
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.get_or_create(recipe=recipe, **ingredient)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        ingredients = validated_data.pop('ingredients', [])
        recipe = super().update(instance, validated_data)
        
        if ingredients:
            recipe.ingredients.all().delete()
            for i in ingredients:
                ingredient = Ingredient.objects.create(name=i['name'])
                recipe.ingredients.add(ingredient)
        instance.save()
        recipe.save()
        recipe.refresh_from_db()
        return recipe