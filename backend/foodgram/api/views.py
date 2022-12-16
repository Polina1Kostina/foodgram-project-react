from .models import Tag, Ingredient, Recipe, IngridientRecipe, ShoppingCart
from .serializers import TagSerializer, IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer, ShoppingCartWriteSerializer
from rest_framework import viewsets
from drf_multiple_serializer import ReadWriteSerializerMixin
from django.shortcuts import get_object_or_404
from rest_framework import mixins


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShoppingCartWriteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ShoppingCartWriteSerializer

    def get_queryset(self):
        recipe_id = self.kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        print(recipe)
        return recipe

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

