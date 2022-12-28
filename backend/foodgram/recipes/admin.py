from django.contrib import admin
from .models import (
    Tag, Ingredient, Recipe, IngridientRecipe, ShoppingCart, FavoriteRecipe,
    TagRecipe)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    list_editable = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(IngridientRecipe)
class IngridientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'amount',
        'ingredients',
        'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(TagRecipe)
class IngridientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'tag',
        'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)
    empty_value_display = '-пусто-'
