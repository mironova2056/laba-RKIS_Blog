from django.urls import path
from .views import (
    profile_view,
    create_post,
    home_view,
    edit_post,
    delete_profile,
    create_comment,
    post_detail,
    register,
    user_login,
    user_logout,
)

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('create_post/', create_post, name='create_post'),
    path('', home_view, name='home'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('create_comment/<int:post_id>/', create_comment, name='create_comment'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),  # Новый маршрут для входа
    path('logout/', user_logout, name='logout'),
]