from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes)
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_multiple_serializer import ReadWriteSerializerMixin
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from recipes.models import (
    Tag, Ingredient, Recipe, IngridientRecipe, ShoppingCart, FavoriteRecipe)
from users.models import Subscription
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeReadSerializer,
    RecipeWriteSerializer, ShoppingCartWriteSerializer,
    FavoriteRecipeWriteSerializer, RecipeViewSerializer,
    SubscriptionReadSerializer)
from .permissions import IsAdminAuthorOrReadOnly, OnlyAuthor, IsAdminOrReadOnly
from .filters import RecipeFilter
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication


class TagViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    """Отображает тэги"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = None


class RecipeViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """Отображает, создает, изменяет и удаляет рецепты"""
    queryset = Recipe.objects.all()
    serializer_classes = {
        'read': RecipeReadSerializer,
        'write': RecipeWriteSerializer,
    }
    permission_classes = [IsAdminAuthorOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@authentication_classes([TokenAuthentication, ])
@login_required
def download_shopping_cart(request):
    """Скачивает список покупок с необходимыми ингридиентами в формате .txt"""
    response = HttpResponse(content_type='text/plain, charset=utf8')
    response['Content-Disposition'] = 'attachment; filename=products.txt'
    user = request.user
    recipes = ShoppingCart.objects.filter(user=user)
    lines = []
    for recipe in recipes:
        ingridients = get_list_or_404(
            IngridientRecipe, recipe_id=recipe.recipe.id)
        ingredient_list = ''
        for ingridient in ingridients:
            ingredient_list += (
                f'{ingridient.ingredients.name} '
                f'({ingridient.ingredients.measurement_unit}) - '
                f'{ingridient.amount} \n')
        lines.append(f'{recipe}: \n{ingredient_list}\n')
    response.writelines(lines)
    return response


@authentication_classes([TokenAuthentication, ])
@api_view(['DELETE', 'POST'])
@permission_classes([OnlyAuthor])
def shopping_cart(request, recipe_id):
    """Добавляет и удаляет рецепт из списка покупок"""
    if request.method == 'POST':
        recipe = Recipe.objects.get(id=recipe_id)
        serializer_view = RecipeViewSerializer(
            data=request.data,
            instance=recipe)
        serializer_create = ShoppingCartWriteSerializer(
            data={
                'user': request.user.id,
                'recipe': recipe_id
            })
        if serializer_create.is_valid(raise_exception=True):
            ShoppingCart.objects.create(recipe_id=recipe.id, user=request.user)
        if serializer_view.is_valid():
            serializer_view.save()
            return Response(
                serializer_view.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        get_object_or_404(ShoppingCart, recipe_id=recipe_id).delete()
        return Response()


@authentication_classes([TokenAuthentication, ])
@api_view(['DELETE', 'POST'])
@permission_classes([OnlyAuthor])
def favorite(request, recipe_id):
    """Добавляет и удаляет рецепт из списка избранного"""
    if request.method == 'POST':
        recipe = Recipe.objects.get(id=recipe_id)
        serializer_view = RecipeViewSerializer(
            data=request.data,
            instance=recipe)
        serializer_create = FavoriteRecipeWriteSerializer(
            data={
                'user': request.user.id,
                'recipe': recipe.id
            })
        if serializer_create.is_valid(raise_exception=True):
            FavoriteRecipe.objects.create(
                recipe_id=recipe.id,
                user=request.user)
        if serializer_view.is_valid():
            serializer_view.save()
            return Response(
                serializer_view.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        get_object_or_404(FavoriteRecipe, recipe_id=recipe_id).delete()
        return Response()


@authentication_classes([TokenAuthentication, ])
class SubscriptionReadViewSet(viewsets.ReadOnlyModelViewSet):
    """Отображает список подписок"""
    serializer_class = SubscriptionReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        new_queryset = get_list_or_404(Subscription, user=self.request.user)
        return new_queryset


@authentication_classes([TokenAuthentication, ])
@api_view(['DELETE', 'POST'])
@permission_classes([OnlyAuthor])
def subscription(request, subscription_id):
    """Добавляет и удаляет пользователя из списка подписок"""
    if request.method == 'POST':
        serializer = SubscriptionReadSerializer(
            data={
                'user': request.user.id,
                'subscription': subscription_id
            })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        get_object_or_404(
            Subscription, subscription_id=subscription_id,
            user=request.user).delete()
        return Response()


class IngredientViewSet(TagViewSet):
    """Отображает список ингридиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^name',)
