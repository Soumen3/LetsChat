from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='home'),
    path('chat/<str:username>',views.chatPage, name='chat'),
    path('user_signup/',views.user_singup, name='user_signup')
]
