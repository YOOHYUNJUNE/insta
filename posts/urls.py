from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/comments/create/', views.comment_create, name='comment_create'),

    path('<int:post_id>/edit/', views.edit, name='edit'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),

    path('<int:post_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    path('<int:post_id>/like', views.like, name='like'),
    path('<int:post_id>/like-async/', views.like_async, name='like_async'),

]