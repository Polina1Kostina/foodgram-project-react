from django.contrib import admin
from .models import Tag, Ingredient, Recipe, IngridientRecipe, ShoppingCart


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
        'id',
        'name',
        'author',
    )
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    list_editable = ('name',)
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


@admin.register(ShoppingCart)
class IngridientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    list_editable = ('recipe',)
    empty_value_display = '-пусто-'