from django.contrib.auth.models import User, auth, Group
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response


def index(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['username']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        type = request.POST['type']

        if pass1 == pass2:
            user = User.objects.create_user(username=name, password=pass1)
            user.save()
            if type =='employee':
                group = Group.objects.get(name='employee')
                group.user_set.add(user)
            if type =='staff':
                group = Group.objects.get(name='staff')
                group.user_set.add(user)
            return redirect('/')
        else:
            return HttpResponse('Password incorrect')
    else:
        return render(request, 'signup.html')



def signin(request):
    if request.method == 'POST':
        name = request.POST['username']
        pass1 = request.POST['password']
        user = auth.authenticate(username=name, password=pass1)
        if user.groups.filter(name='employee').exists():
            auth.login(request, user)
            return redirect('/')
        elif user.groups.filter(name='staff').exists():
            auth.login(request, user)
            print(user.groups.name)
            return redirect('/staffhome')

    else:
        return render(request, 'signin.html')


def signout(request):
    auth.logout(request)
    print('Sucess...')
    return redirect('/')

def staffhome(request):
    if request.user.groups.filter(name='staff').exists():
        return render(request, 'staffhome.html')
    else:
        raise PermissionDenied