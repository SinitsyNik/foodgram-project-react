from django.shortcuts import get_object_or_404, HttpResponse
from djoser.views import UserViewSet
from django.db.models import Sum
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .pagination import LimitPageNumberPagination
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, SubscribeSerializer,
                          MiniRecipeSerializer)
from users.models import Follow
from recipes.models import (Ingredient, RecipeIngredient, Recipe,
                            ShoppingCart, Tag, Favorite)


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response(
                {'errors': 'Вы не можете подписываться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response(
                {'errors': 'Вы уже подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Follow.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписываться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы уже отписались'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        instance = Favorite.objects.filter(user=request.user, recipe__id=pk)
        if request.method == 'POST' and not instance.exists():
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        instance = ShoppingCart.objects.filter(
            user=request.user,
            recipe__id=pk
        )
        if request.method == 'POST' and not instance.exists():
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values(
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
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
