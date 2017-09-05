from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from sevchefs_api.utils import RecipeUtils
from sevchefs_api.utils import get_request_body_param


class CommentRecipeView(APIView):

    @method_decorator(login_required)
    def post(self, request, pk):
        """
        Login user comment on a recipe

        @body comment: user comment on the recipe
        @return: http status of query
        @raise HTTP_401_UNAUTHORIZED: user must be login
        @raise HTTP_404_NOT_FOUND: must be a valid recipe id
        @raise HTTP_400_BAD_REQUEST: recipe comment must not be empty
        """

        comment = get_request_body_param(request, 'comment').strip()
        if comment == "":
            return Response({'detail': 'recipe comment must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        recipe = RecipeUtils.get_recipe_or_404(pk)
        comment_user = request.user

        RecipeUtils.add_recipe_comments(recipe, comment_user, comment)

        return Response({'data': 'success'}, status=status.HTTP_201_CREATED)


class RecipeView(APIView):
    def post(self, request):
        pass


class RecipeIngredientView(APIView):
    pass
