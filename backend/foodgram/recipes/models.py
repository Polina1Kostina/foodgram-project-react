from django.db import models
from colorfield.fields import ColorField
from users.models import User
from django.core.validators import RegexValidator, MinValueValidator


class Tag(models.Model):
    """Тэги рецептов"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё]*$',
                message='Название может состоять только из русских букв',
            )])
    color = ColorField(
        default='#FF0000',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Код цвета передан в неверном формате',
            )])
    slug = models.SlugField(
        max_length=150,
        blank=False,
        unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    """Ингридиенты для рецептов"""
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
    """Рецепты с указанием количества ингридиента"""
    amount = models.PositiveIntegerField()
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ingredients} {self.amount}'

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Рецепт Ингридиент'
        verbose_name_plural = 'Рецепты и ингридиенты с количеством'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'ingredients', 'recipe'), name='unique ingredients recipe'
            )
        ]


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through=IngridientRecipe)
    tags = models.ManyToManyField(Tag, through='TagRecipe', blank=False)
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1, message='Укажите время приготовления больше 1 минуты'),
        ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagRecipe(models.Model):
    """Рецепты с указанием тэгов"""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('tag', 'recipe'), name='unique tag recipe'
            )
        ]


class ShoppingCart(models.Model):
    """Список покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopuser')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart')

    def __str__(self):
        return f'{self.recipe.name}'

    class Meta:
        ordering = ('user',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique shopping cart'
            )
        ]


class FavoriteRecipe(models.Model):
    """Избранные рецепты"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='userfavorite')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite')

    def __str__(self):
        return f'{self.recipe.name}'

    class Meta:
        ordering = ('user',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique favorite recipe'
            )
        ]
