from django.db import models
from colorfield.fields import ColorField
from users.models import User


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(
        max_length=150,
        blank=False,
        unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'



class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    measurement_unit = models.CharField(max_length=100, blank=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
    
    def __str__(self):
        return self.name


class IngridientRecipe(models.Model):
    amount = models.IntegerField()
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)


class Recipe(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipe/', null=True, blank=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through=IngridientRecipe,)
    tags = models.ManyToManyField(Tag, through="TagRecipe", blank=False)
    cooking_time = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='shopp')

    def __str__(self):
        return f'{self.user} {self.recipe}'