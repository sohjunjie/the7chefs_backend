from django.conf.urls import url
from sevchefs_api import views

urlpatterns = [
    url(r'api/v1.0/comment/recipe/(?P<pk>[0-9]+)/$', views.CommentRecipeView.as_view(), name="comment-recipe"),
]
