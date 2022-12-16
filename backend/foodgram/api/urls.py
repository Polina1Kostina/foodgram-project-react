from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import TagViewSet, IngredientViewSet, RecipeViewSet, ShoppingCartWriteViewSet

router = routers.DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartWriteViewSet, basename='shopping_cart')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
