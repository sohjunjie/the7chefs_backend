from django.conf.urls import url
from sevchefs_api import views

urlpatterns = [

    url(r'api/v1.0/recipe/(?P<pk>[0-9]+)/$', views.RecipeView.as_view(), name="recipe-view"),
    url(r'api/v1.0/recipe/list/$', views.RecipeListView.as_view(), name="recipe-list-view"),
    url(r'api/v1.0/recipe/upload/$', views.RecipeUploadView.as_view(), name="recipe-upload"),
    url(r'api/v1.0/recipe/comment/(?P<pk>[0-9]+)/$', views.CommentRecipeView.as_view(), name="recipe-comment"),
    url(r'api/v1.0/recipe/add/tag/(?P<pk>[0-9]+)/$', views.RecipeAddTagView.as_view(), name="recipe-add-tag"),
    url(r'api/v1.0/recipe/image/upload/(?P<pk>[0-9]+)/$', views.RecipeImageUploadView.as_view(), name="recipe-image-upload"),

    url(r'api/v1.0/user/signup/$', views.UserSignUpView.as_view(), name="user-signup"),
    url(r'api/v1.0/user/all/$', views.UserProfileListView.as_view(), name="user-all-detail"),
    url(r'api/v1.0/user/profile/(?P<pk>[0-9]+)/$', views.UserProfileView.as_view(), name="user-profile-detail"),

]
