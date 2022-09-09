from django.contrib import admin

from .models import (Ingredient, Recipe, Tag, RecipeIngredient,
                     Favorite, ShoppingCart)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra: int = 1
    verbose_name_plural = 'Ингредиенты'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('name', 'author',)
    search_fields = ('name', 'author')
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientsInline, )

    def count_in_favorites(self, recipe):
        return Favorite.objects.filter(recipe=recipe).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(RecipeIngredient)
