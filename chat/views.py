from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import ChatModel
# Create your views here.
User= get_user_model()

def index(request):
    context={}
    users=User.objects.exclude(username=request.user.username)
    context['users']=users
    return render(request,'index.html',context)

def chatPage(request, username):
    context={}
    user_obj=User.objects.get(username=username)
    user=User.objects.exclude(username=request.user.username)
    context['user']=user_obj
    context['users'] = user

    if request.user.id > user_obj.id:
        thread_name=f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name=f'chat_{user_obj.id}-{request.user.id}'
    message_obj=ChatModel.objects.filter(thread_name=thread_name)
    context['messages']=message_obj
    
    return render(request, 'main_chat.html', context)