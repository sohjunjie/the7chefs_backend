from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from sevchefs_api.models import Ingredient
from sevchefs_api.serializers import IngredientSerializer


class IngredientListView(generics.ListAPIView):
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        ingredient_list = Ingredient.objects.all()
        return ingredient_list

    def get_serializer_context(self):
        return {'request': self.request}
