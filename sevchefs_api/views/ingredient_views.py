from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from sevchefs_api.models import Ingredient
from sevchefs_api.serializers import IngredientSerializer


class IngredientListView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = IngredientSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
