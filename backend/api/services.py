from django.db.models import Sum

from recipes.models import RecipeIngredient


def count_shopping_cart(user):
    ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=user).values(
        'ingredient__name',
        'ingredient__measurement_unit').annotate(amount=Sum('amount'))
    shopping_cart = (
        'Список покупок.\n\n'
    )
    for ingredient in ingredients:
        shopping_cart += (
            f'{ingredient["ingredient__name"]}: {ingredient["amount"]}'
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )
    return shopping_cart
