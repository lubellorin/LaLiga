from django.urls import path

from core.user.views import *

app_name = 'user'

urlpatterns = [
    # Usuarios
    path('list/', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('groups/<int:pk>/', UserUpdateGroupsView.as_view(), name='user_groups'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('change/password/', UserChangePasswordView.as_view(), name='user_change_password'),
    path('change/group/<int:pk>/', UserChangeGroup.as_view(), name='user_change_group'),
]
