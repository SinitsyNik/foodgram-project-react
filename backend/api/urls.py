from django.urls import include, path
from rest_framework import routers

from .views import (
    TagViewSet, RecipeViewSet, IngredientViewSet, CustomUserViewSet
)


app_name = 'api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
