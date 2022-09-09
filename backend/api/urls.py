from django.urls import include, path
from rest_framework import routers

from .views import (TagsViewSet, RecipeViewSet,
                    IngredientsViewSet, CustomUserViewSet)


app_name = 'api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('tags', TagsViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
