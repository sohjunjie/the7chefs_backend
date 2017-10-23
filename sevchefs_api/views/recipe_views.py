from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from sevchefs_api.models import Recipe, RecipeTagTable, UserRecipeFavourites, \
    RecipeIngredient, RecipeInstruction
from sevchefs_api.serializers import RecipeSerializer, RecipeImageSerializer, \
    RecipeIngredientSerializer, RecipeInstructionImageSerializer

from sevchefs_api.utils import RecipeUtils, UserUtils
from sevchefs_api.utils import get_request_body_param


class FavouritedRecipeListView(generics.ListAPIView):

    serializer_class = RecipeSerializer

    @permission_classes((IsAuthenticated, ))
    def list(self, request):
        user = request.user
        fav_recipes = user.userprofile.favourited_recipes.all()
        serializer = RecipeSerializer(fav_recipes, many=True, context={'request': request})
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class FavouriteRecipeView(APIView):
    def post(self, request, pk):
        """
        Login user favourite on a recipe by id

        @return: http status of query
        @raise HTTP_401_UNAUTHORIZED: user must be login
        @raise HTTP_404_NOT_FOUND: must be a valid recipe id
        """

        recipe = RecipeUtils.get_recipe_or_404(pk)
        userprofile = request.user.userprofile
        UserRecipeFavourites.objects.create(userprofile=userprofile, recipe=recipe)

        return Response({"success": True}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """
        Login user can unfavourite recipe by id
        """
        recipe = RecipeUtils.get_recipe_or_404(pk)
        userprofile = request.user.userprofile
        recipe_favouited = UserRecipeFavourites.objects.filter(userprofile=userprofile, recipe=recipe)
        recipe_favouited.delete()

        return Response({"success": True}, status=status.HTTP_200_OK)


class CommentRecipeView(APIView):

    def post(self, request, pk):
        """
        Login user comment on a recipe by id

        @body comment: user comment on the recipe
        @return: http status of query
        @raise HTTP_401_UNAUTHORIZED: user must be login
        @raise HTTP_404_NOT_FOUND: must be a valid recipe id
        @raise HTTP_400_BAD_REQUEST: recipe comment must not be empty
        """

        comment = get_request_body_param(request, 'comment', '').strip()
        if not comment:
            return Response({'detail': 'recipe comment must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        recipe = RecipeUtils.get_recipe_or_404(pk)
        comment_user = request.user

        RecipeUtils.add_recipe_comments(recipe, comment_user, comment)

        return Response({"success": True}, status=status.HTTP_201_CREATED)


class RecipeView(APIView):

    @permission_classes((AllowAny, ))
    def get(self, request, pk):
        """
        View recipe details by id
        """
        recipe = RecipeUtils.get_recipe_or_404(pk)
        serializer = RecipeSerializer(recipe)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):

        recipe = RecipeUtils.get_recipe_or_404(pk)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe, request)

        r_name = get_request_body_param(request, 'name', None)
        r_desc = get_request_body_param(request, 'description', None)
        r_diff_level = get_request_body_param(request, 'difficulty_level', None)

        if r_name is not None:
            recipe.name = r_name

        if r_desc is not None:
            recipe.description = r_desc

        if r_diff_level is not None:
            recipe.difficulty_level = r_diff_level

        recipe.save()
        return Response({'success': True}, status=status.HTTP_200_OK)


class UserRecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)

    def list(self, request, pk):
        user = UserUtils.get_user_or_404(pk)
        recipes = self.get_queryset()
        recipes = recipes.filter(upload_by_user=user)
        serializer = RecipeSerializer(recipes, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# TODO: ADD IN API DOCS
class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RecipeSerializer(queryset, many=True, context={'request': request})
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class RecipeUploadView(APIView):

    def post(self, request):
        """
        Create an empty recipe

        @body str name: recipe name
        @body str description: recipe description
        @body int difficulty: difficulty level from 1 - 5
        """
        recipe_name = get_request_body_param(request, 'name', '').strip()
        recipe_desc = get_request_body_param(request, 'description', '').strip()
        recipe_diff = get_request_body_param(request, 'difficulty', 0)
        # duration_minute = get_request_body_param(request, 'duration_minute', 0)
        # duration_hour = get_request_body_param(request, 'duration_hour', 0)

        if recipe_name == "":
            return Response({'detail': 'recipe name must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if recipe_desc == "":
            return Response({'detail': 'recipe desc must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        recipe_diff = recipe_diff if isinstance(recipe_diff, int) else 0

        upload_user = request.user

        recipe = Recipe.objects.create(name=recipe_name, description=recipe_desc,
                                       difficulty_level=recipe_diff,
                                       upload_by_user=upload_user)

        return Response({"success": True, "recipe_id": recipe.id}, status=status.HTTP_201_CREATED)


# TODO: TEST
class RecipeAddTagView(APIView):

    def post(self, request, pk):
        """
        Add tags to a recipe

        @body int[] tag_ids: list of tag id
        @raise HTTP_401_UNAUTHORIZED: only creator of recipe can add tag to recipe
        """

        recipe = RecipeUtils.get_recipe_or_404(pk)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe, request)

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

    def post(self, request, pk):

        recipe = RecipeUtils.get_recipe_or_404(pk)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe, request)

        serializer = RecipeImageSerializer(recipe, data=request.data)
        if serializer.is_valid():
            RecipeUtils.delete_recipe_image(recipe)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        recipe = RecipeUtils.get_recipe_or_404(pk)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe, request)

        RecipeUtils.delete_recipe_image(recipe)
        return Response({"success": True}, status=status.HTTP_200_OK)


class RecipeInstructionView(APIView):
    def post(self, request):
        r_id = get_request_body_param(request, 'recipe_id', None)
        r_step_num = get_request_body_param(request, 'step_num', 0)
        r_instr_text = get_request_body_param(request, 'instruction', None)
        r_dur_min = get_request_body_param(request, 'duration_minute', 0)
        r_dur_hour = get_request_body_param(request, 'duration_hour', 0)

        recipe = RecipeUtils.get_recipe_or_404(r_id)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe, request)

        if r_step_num <= 0:
            return Response({'detail': 'Step number must be greater or equal to 1'}, status=status.HTTP_400_BAD_REQUEST)
        if not r_instr_text:
            return Response({'detail': 'Instruction for recipe must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        r_dur_min = r_dur_min if isinstance(r_dur_min, int) else 0
        r_dur_hour = int(r_dur_hour) if isinstance(r_dur_hour, int) else 0
        r_duration = timedelta(hours=r_dur_hour, minutes=r_dur_min)

        ri = RecipeInstruction.objects.create(recipe=recipe, step_num=r_step_num, instruction=r_instr_text, time_required=r_duration)
        return Response({"success": True, "instruction_id": ri.id}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pass


class RecipeInstructionImageView(APIView):
    def post(self, request, pk):

        recipe_instruction = RecipeUtils.get_recipe_instruction_or_404(pk)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe_instruction.recipe, request)

        serializer = RecipeInstructionImageSerializer(recipe_instruction, data=request.data)
        if serializer.is_valid():
            RecipeUtils.delete_recipe_instruction_image(recipe_instruction)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeIngredientView(APIView):
    def post(self, request, rpk, ipk):
        """
        Add ingredient to recipe
        """
        serving_size = get_request_body_param(request, 'serving_size', '').strip()
        if not serving_size:
            return Response({'detail': 'serving size of ingredient must not be empty'}, status=status.HTTP_400_BAD_REQUEST)

        recipe = RecipeUtils.get_recipe_or_404(rpk)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe, request)

        ingredient = RecipeUtils.get_ingredient_or_404(ipk)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, serving_size=serving_size)

        return Response({"success": True}, status=status.HTTP_201_CREATED)

    def delete(self, request, rpk, ipk):
        """
        delete ingredient from recipe
        """
        recipe = RecipeUtils.get_recipe_or_404(rpk)
        RecipeUtils.raise_401_if_recipe_not_belong_user(recipe, request)

        ingredient = RecipeUtils.get_ingredient_or_404(ipk)
        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).first()
        recipe_ingredient.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
