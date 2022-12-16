from rest_framework import serializers
from .models import TagRecipe, Ingredient, Recipe, IngridientRecipe, Tag, ShoppingCart
from users.serializers import UserRegistrationSerializer
from drf_writable_nested import WritableNestedModelSerializer
from users.models import User

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id',)
        read_only_fields = ('name', 'measurement_unit',)


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngridientRecipe
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = IngredientRecipeSerializer(many=True, source='ingridientrecipe_set',)

    class Meta:
        ordering = ['-id']
        model = Recipe
        fields = ['ingredients', 'image', 'name', 'text', 'cooking_time', 'tags']

    def create(self, validated_data):
        ingri_data = dict(validated_data.pop('ingridientrecipe_set')[0])
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        IngridientRecipe.objects.create(ingredients_id = ingri_data['id'], recipe_id=recipe.id, amount=ingri_data['amount'])
        for tag_data in tags_data:
            TagRecipe.objects.create(tag_id=tag_data.id, recipe=recipe)
        return recipe


class RecipeReadSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Recipe
        fields = '__all__'


class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    #image = serializers.ReadOnlyField(source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ['id', 'name', 'cooking_time', ]
