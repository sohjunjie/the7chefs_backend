from random import randint

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from sevchefs_api.models import Recipe
from sevchefs_api.serializers import RecipeSerializer


class RecommendRecipeView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        recipes = Recipe.objects.all()
        if not request.user.is_anonymous():
            recipes = recipes.exclude(upload_by_user=request.user)

        if recipes.count() <= 0:
            return Response({"data": None}, status=status.HTTP_200_OK)

        min = 0
        max = recipes.count() - 1
        recommended = recipes[randint(min, max)]
        serializer = RecipeSerializer(recommended)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
