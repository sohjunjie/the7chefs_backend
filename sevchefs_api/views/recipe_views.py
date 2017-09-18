from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from sevchefs_api.models import Recipe, RecipeTagTable
from sevchefs_api.serializers import RecipeSerializer, RecipeImageSerializer
from sevchefs_api.utils import RecipeUtils
from sevchefs_api.utils import get_request_body_param
# from rest_framework.decorators import permission_classes
# @permission_classes((IsAuthenticated, ))


class CommentRecipeView(APIView):

    def post(self, request, pk):
        """
        Login user comment on a recipe

        @body comment: user comment on the recipe
        @return: http status of query
        @raise HTTP_401_UNAUTHORIZED: user must be login
        @raise HTTP_404_NOT_FOUND: must be a valid recipe id
        @raise HTTP_400_BAD_REQUEST: recipe comment must not be empty
        """

        comment = get_request_body_param(request, 'comment', '').strip()
        if comment == "":
            return Response({'detail': 'recipe comment must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        recipe = RecipeUtils.get_recipe_or_404(pk)
        comment_user = request.user

        RecipeUtils.add_recipe_comments(recipe, comment_user, comment)

        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)


class RecipeView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, pk):
        """
        View recipe details by id
        """
        recipe = RecipeUtils.get_recipe_or_404(pk)
        serializer = RecipeSerializer(recipe)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# TODO: ADD IN API DOCS
class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RecipeSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class RecipeUploadView(APIView):

    def post(self, request):
        """
        Create an empty recipe

        @body str name: recipe name
        @body str description: recipe description
        @body int difficulty: difficulty level from 1 - 5
        @body int duration_minute
        @body int duration_hour
        """
        recipe_name = get_request_body_param(request, 'name', '').strip()
        recipe_desc = get_request_body_param(request, 'description', '').strip()
        recipe_diff = get_request_body_param(request, 'difficulty', 0)
        duration_minute = get_request_body_param(request, 'duration_minute', 0)
        duration_hour = get_request_body_param(request, 'duration_hour', 0)

        if recipe_name == "":
            return Response({'detail': 'recipe name must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if recipe_desc == "":
            return Response({'detail': 'recipe desc must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        recipe_diff = recipe_diff if isinstance(recipe_diff, int) else 0
        duration_minute = duration_minute if isinstance(duration_minute, int) else 0
        duration_hour = int(duration_hour) if isinstance(duration_hour, int) else 0

        recipe_duration = timedelta(hours=duration_hour, minutes=duration_minute)

        upload_user = request.user

        Recipe.objects.create(name=recipe_name, description=recipe_desc,
                              difficulty_level=recipe_diff,
                              time_required=recipe_duration,
                              upload_by_user=upload_user)

        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)


# TODO: TEST
class RecipeAddTagView(APIView):

    def post(self, request, pk):
        """
        Add tags to a recipe

        @body int[] tag_ids: list of tag id
        @raise HTTP_401_UNAUTHORIZED: only creator of recipe can add tag to recipe
        """

        recipe = RecipeUtils.get_recipe_or_404(pk)
        if recipe.upload_by_user != request.user:
            return Response({'detail': 'only creator of recipe can add tag to recipe'},
                            status=status.HTTP_401_UNAUTHORIZED)

        tag_ids = get_request_body_param(request, 'tag_ids', [])

        tag_ids_added = []
        for tag_id in tag_ids:
            tag = RecipeUtils.get_recipe_tag_or_none(tag_id)
            if tag is not None:
                RecipeTagTable.objects.create(recipe=recipe, tag=tag)
                tag_ids_added.append(tag_id)

        response_data = {'tag_ids_added': tag_ids_added,
                         'tag_ids_not_added': list(set(tag_ids) - set(tag_ids_added))}

        return Response({'data': response_data}, status=status.HTTP_201_CREATED)


class RecipeImageUploadView(APIView):

    # def put(self, request, pk, format=None):
    def put(self, request, pk):

        print(request.data)

        recipe = RecipeUtils.get_recipe_or_404(pk)
        serializer = RecipeImageSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeIngredientView(APIView):
    pass
