from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    ORANGE = '#E26C2D'
    GREEN = '#49B64E'
    PURPLE = '#8775D2'

    COLOR_CHOICES = [
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
    ]
    name = models.CharField(
        max_length=20,
        verbose_name='Название тэга',
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код',
        choices=COLOR_CHOICES,
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=20,
        verbose_name='Уникальный слаг',
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Тэг',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1, message='Минимальное время приготовления 1 минута'),
        ]
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        ordering = ['user', 'recipe']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='shopping_cart_unique')
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        ordering = ['user', 'recipe']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='favorite_unique')
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )
    amount = models.FloatField(
        verbose_name='Количество',
        default=1,
        validators=[MinValueValidator(
            0.1, message='Минимальное количество ингридиентов 0.1'),
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиента в рецепте'

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'
