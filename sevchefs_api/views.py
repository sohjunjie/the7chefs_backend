from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from sevchefs_api.utils import RecipeUtils


class CommentRecipeView(APIView):

    @method_decorator(login_required)
    def post(self, request, pk):
        """ 401 unauthorized error if not login """
        comment_user = request.user
        recipe = RecipeUtils.get_recipe_or_404()

        return Response({'data': "success"}, status=status.HTTP_200_OK)


# @login_required     # HTTP_403_FORBIDDEN return if not login
# @ensure_csrf_cookie
# class CommentRecipeView(APIView):
#
#     def post(self, request):
#         # username = request.user.username
#         # return Response({'data': username}, status=status.HTTP_200_OK)
#         return Response('data', status=status.HTTP_200_OK)
