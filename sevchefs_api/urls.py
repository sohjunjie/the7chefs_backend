from django.conf.urls import url
from sevchefs_api import views

urlpatterns = [

    url(r'^api/v1.0/login2', views.ObtainAuthToken.as_view(), name="auth-token-view"),

    url(r'api/v1.0/recipe/(?P<pk>[0-9]+)/$', views.RecipeView.as_view(), name="recipe-view"),
    url(r'api/v1.0/recipe/(?P<rpk>[0-9]+)/ingredient/(?P<ipk>[0-9]+)/$', views.RecipeIngredientView.as_view(), name="recipe-ingredient"),

    url(r'api/v1.0/recipe/list/$', views.RecipeListView.as_view(), name="recipe-list-view"),
    url(r'api/v1.0/recipe/upload/$', views.RecipeUploadView.as_view(), name="recipe-upload"),
    url(r'api/v1.0/recipe/comment/(?P<pk>[0-9]+)/$', views.CommentRecipeView.as_view(), name="recipe-comment"),
    url(r'api/v1.0/recipe/favourite/(?P<pk>[0-9]+)/$', views.FavouriteRecipeView.as_view(), name="recipe-favourite"),
    url(r'api/v1.0/recipe/add/tag/(?P<pk>[0-9]+)/$', views.RecipeAddTagView.as_view(), name="recipe-add-tag"),
    url(r'api/v1.0/recipe/image/upload/(?P<pk>[0-9]+)/$', views.RecipeImageUploadView.as_view(), name="recipe-image-upload"),

    url(r'api/v1.0/recipe/instruction/$', views.RecipeInstructionView.as_view(), name="recipe-instruction-view"),
    url(r'api/v1.0/recipe/instruction/image/upload/(?P<pk>[0-9]+)/$', views.RecipeInstructionImageView.as_view(), name="recipe-instruction-image-upload"),

    url(r'api/v1.0/user/(?P<pk>[0-9]+)/recipe/list/$', views.UserRecipeListView.as_view(), name="user-recipe-list"),

    url(r'api/v1.0/user/signup/$', views.UserSignUpView.as_view(), name="user-signup"),
    url(r'api/v1.0/user/all/$', views.UserProfileListView.as_view(), name="user-all-detail"),
    url(r'api/v1.0/user/profile/(?P<pk>[0-9]+)/$', views.UserProfileView.as_view(), name="user-profile-detail"),

    url(r'^api/v1.0/follow/user/(?P<pk>.+)/$', views.FollowUserView.as_view(), name='user-follow'),

]
