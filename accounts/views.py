from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': [],
    }

    for post in posts:
        user = User.objects.get(username=post.user)
        profile = Profile.objects.get(user=user)
        profile_img_url = settings.MEDIA_URL + str(profile.profileimg)
        
        post_data = {
            'post': post,
            'profile_img_url': profile_img_url,
        }
        context['posts'].append(post_data)

    return render(request, 'auth/index.html', context)

        # print(profile_img_url)

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
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
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

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        

        messages.success(request, 'Your post has been uploaded successfully.')

        return redirect('/')
    else:
        return render(request, 'auth/post_upload.html')
    
def dislike(request,post_id):

    print("going in to dislike")

    username = request.user.username
    post = Post.objects.get(id=post_id)
    like_filter = DisLikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = DisLikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_dislikes = post.no_of_dislikes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_dislikes = post.no_of_dislikes-1
        post.save()
        return redirect('/')
def like(request,post_id):

    print("going in to like")

    username = request.user.username
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
