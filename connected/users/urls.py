from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('add-skills/', views.addSkill, name='add-skill'),
    path('update-skills/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete-skills/<str:pk>/', views.deleteSkill, name='delete-skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('messages/<str:pk>/', views.viewMessage, name='viewMessage'),
    path('send-message/<str:pk>', views.sendMessage, name='sendMessage'),
]

