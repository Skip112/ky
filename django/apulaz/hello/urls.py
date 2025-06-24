from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forum/', views.forum, name='forum'),
    path('forum/create/', views.create_topic, name='create_topic'),
    path('forum/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_utilites/', views.admin_utilites, name='admin_utilites'),
    path('admin-dashboard/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin-dashboard/reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('admin-dashboard/grant-admin-rights/<int:user_id>/', views.grant_admin_rights, name='grant_admin_rights'),
    path('admin-dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-dashboard/block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('admin-dashboard/unblock-user/<int:user_id>/', views.unblock_user, name='unblock_user'), 
]