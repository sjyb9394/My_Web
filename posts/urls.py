from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('<int:pk>/', views.post_detail.as_view(), name="detail"),
    path('<int:pk>/comment/', views.add_comment_to_post, name="add_comment"),
    path('new_post/', views.create_post, name="new_post"),
    path('<int:pk>/detail/modify', views.post_modify, name="modify"),
    path('<int:pk>/post/delete/', views.post_delete, name="post_delete"),
    path('<int:pk>/comment/delete/', views.comment_delete, name="comment_delete"),
    path('<int:pk>/post/vote/', views.vote_post, name="vote_post"),
    path('<int:pk>/post/vote_comment/', views.vote_comment, name="vote_comment"),
]