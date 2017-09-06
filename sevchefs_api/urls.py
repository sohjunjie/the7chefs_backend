from django.conf.urls import url
from sevchefs_api import views

urlpatterns = [
    url(r'api/v1.0/recipe/(?P<pk>[0-9]+)/$', views.RecipeView.as_view(), name="recipe-view"),
    url(r'api/v1.0/recipe/upload/$', views.RecipeUploadView.as_view(), name="recipe-upload"),
    url(r'api/v1.0/recipe/comment/(?P<pk>[0-9]+)/$', views.CommentRecipeView.as_view(), name="recipe-comment"),

    url(r'api/v1.0/user/signup/$', views.UserSignUpView.as_view(), name="user-signup"),

]
