from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (
    TagRecipe, Ingredient, Recipe, IngridientRecipe, Tag, ShoppingCart,
    FavoriteRecipe)
from users.models import User, Subscription
from django.db import transaction


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='ingredients.id', required=True)
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngridientRecipe
        fields = ('id', 'amount', 'name', 'measurement_unit')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        try:
            is_subscribed = user.subscrib.filter(
                subscription=obj.id).exists()
            return is_subscribed
        except TypeError:
            return False

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_subscribed')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingridientrecipe_set')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        try:
            is_favorited = user.userfavorite.filter(
                recipe=obj.id).exists()
            return is_favorited
        except TypeError:
            return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        try:
            is_in_shopping_cart = user.shopuser.filter(
                recipe=obj.id).exists()
            return is_in_shopping_cart
        except TypeError:
            return False

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'image',
                  'id', 'tags', 'ingredients', 'name', 'text', 'cooking_time')


class RecipeWriteSerializer(RecipeReadSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingridientrecipe_set',)

    def validate_ingredients(self, value):
        for v in value:
            try:
                ing_id = v['ingredients']['id']
            except ValidationError:
                raise serializers.ValidationError(
                    'Ошибка при передаче id ингридиента')
            if not Ingredient.objects.filter(id=ing_id).exists():
                raise serializers.ValidationError(
                    f'Ингридиент с id-{ing_id} не найден')
            return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingridientrecipe_set')
        tags_data = validated_data.pop('tags')
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                for tag_data in tags_data:
                    recipe = Recipe.objects.create(**validated_data)
                    TagRecipe.objects.create(tag_id=tag_data.id, recipe=recipe)
                for ingredient_data in ingredients_data:
                    ingredients_id = ingredient_data.pop('ingredients')['id']
                    IngridientRecipe.objects.create(
                        recipe_id=recipe.id,
                        ingredients_id=ingredients_id,
                        **ingredient_data)
                return recipe
            except ValidationError as ex:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError(f'Ошибка:{str(ex)}')
            else:
                transaction.savepoint_commit(sid)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        tags_data = validated_data.pop('tags')
        instance.tags.set(tags_data)
        instance.ingredients.clear()
        ingredients_data = validated_data.pop('ingridientrecipe_set')
        new_ingredients = []
        for ingredient_data in ingredients_data:
            ingredients_id = ingredient_data.pop('ingredients')['id']
            ing, status = IngridientRecipe.objects.get_or_create(
                recipe=instance,
                ingredients_id=ingredients_id,
                **ingredient_data)
            new_ingredients.append(ing)
        instance.ingridientrecipe_set.set(new_ingredients)
        instance.save()
        return instance


class RecipeViewSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    image = serializers.URLField(read_only=True)
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe')
            )
        ]


class FavoriteRecipeWriteSerializer(ShoppingCartWriteSerializer):
    class Meta(ShoppingCartWriteSerializer.Meta):
        model = FavoriteRecipe
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe')
            )
        ]


class SubscriptionReadSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='subscription.email')
    id = serializers.ReadOnlyField(source='subscription.id')
    username = serializers.ReadOnlyField(source='subscription.username')
    first_name = serializers.ReadOnlyField(source='subscription.first_name')
    last_name = serializers.ReadOnlyField(source='subscription.last_name')
    recipes = RecipeViewSerializer(
        many=True, source='subscription.author', read_only=True)
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        recipes_count = Recipe.objects.filter(
            author=obj.subscription.id).count()
        return recipes_count

    class Meta:
        model = Subscription
        fields = (
            'user', 'subscription', 'email', 'id', 'username', 'first_name',
            'last_name', 'recipes', 'recipes_count')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'subscription', )
            )
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
