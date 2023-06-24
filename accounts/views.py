from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request, 'auth/index.html')


@login_required(login_url='/signin')
def signout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    print("goining to signup")

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=pass1)
                user.save()

                # logging in part
                user_login = auth.authenticate(username=username, password=pass1)
                auth.login(request, user_login)

                #creating profile
                user_model = User.objects.get(username=username)
                # new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                # new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'pass1 Not Matching')
            return redirect('/signup')


    return render(request, 'auth/signup.html')


def signin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user==None:
            messages.info(request, 'Credentials Invalid')
            return redirect('/signin')

        else:
            auth.login(request,user)
            return redirect('/')
    return render(request, 'auth/signin.html') 
