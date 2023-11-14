from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import ChatModel
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib import messages


# Create your views here.
User= get_user_model()

@login_required(login_url='login')
def index(request):
    context={}
    users=User.objects.exclude(username=request.user.username)
    context['users']=users
    return render(request,'index.html',context)

@login_required(login_url='login')
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

def user_singup(request):
    if not request.user.is_authenticated:
        context={}
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            form.save()
            messages.success(request, 'You are successfully signed up.')
            return redirect('login')
        else:
            form=SignUpForm()
            context['form']=form
            return render(request, 'registration/signup.html', context)
    else:
        messages.info(request, "You are already Signed In.")
        return redirect('home')