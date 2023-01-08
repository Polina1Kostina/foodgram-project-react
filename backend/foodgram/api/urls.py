from django.urls import include, path, re_path
from rest_framework import routers
from .views import (
    TagViewSet, IngredientViewSet, RecipeViewSet, download_shopping_cart,
    shopping_cart, favorite, SubscriptionReadViewSet, subscription)

router = routers.DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(
    r'users/subscriptions',
    SubscriptionReadViewSet,
    basename='subscriptions_read')

recipes_router = [
    path('download_shopping_cart/', download_shopping_cart),
    path('<recipe_id>/shopping_cart/', shopping_cart),
    path('<recipe_id>/favorite/', favorite),
]

urlpatterns = [
    path('recipes/', include(recipes_router)),
    path('users/<subscription_id>/subscribe/', subscription),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
