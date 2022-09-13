from django.db.models import Sum

from recipes.models import RecipeIngredient


def get_ingredients_for_shopping(user):
    ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=user).order_by(
        'ingredient__name').values(
        'ingredient__name',
        'ingredient__measurement_unit',).annotate(amount=Sum('amount'))
    shopping_cart = '\n'.join([
        f'{ingredient["ingredient__name"]}: {ingredient["amount"]}'
        f'{ingredient["ingredient__measurement_unit"]}'
        for ingredient in ingredients
    ])
    return shopping_cart
