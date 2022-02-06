from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def index(request):
    return render(request,"app/index.html")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            messages.success(request,f'User {username} created')
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request,'app/register.html',context)

#create user and send a signal to save profile
def create_profile(sender,instance,created,**kwards):
    if created:
        Profile.objects.create(name=instance)
post_save.connect(create_profile,sender=User)