# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from datetime import datetime
from django.shortcuts import render, redirect
from datetime import timedelta
from Jproject.settings import BASE_DIR
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from django.contrib.auth.hashers import make_password,check_password
from models import User, SessionToken, PostModel, LikeModel, CommentModel
from django.http import HttpResponse
from django.utils import timezone

from imgurpython import ImgurClient
from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key='d7a0a1a358064837b403d3ca99a6249c')
model = app.models.get('food-items-v1.0')
response = model.predict_by_url(url='https://www.elementstark.com/woocommerce-extension-demos/wp-content/uploads/sites/2/2016/12/pizza.jpg')
print response

# Create your views here.

def signup_view(request):
    if request.method == "POST":
        # print 'Sign up form submitted'
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #save data to db
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')
    elif request.method == 'GET':
        form = SignUpForm()

    today = datetime.date.today()
    return render(request, 'index.html', {'form': form, 'today': today})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()

            if user:
                # Check for the password
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password!'

    elif request.method == "GET":
        form = LoginForm()

    return render(request, 'login.html', response_data)


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()



                path = str(BASE_DIR + post.image.url)

                client = ImgurClient("1d5ea33b83cf0b8","ec342f2708eb4bfede86e5a9bc190684daaf97ad" )
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                clarifai_data = []
                app = ClarifaiApp(api_key='d7a0a1a358064837b403d3ca99a6249c')
                model = app.models.get("general-v1.3")
                result = model.predict_by_url(url=post.image_url)
                for x in range(0, len(result['outputs'][0]['data']['concepts'])):
                    model = result['outputs'][0]['data']['concepts'][x]['name']
                    clarifai_data.append(model)
                for z in range(0, len(clarifai_data)):
                    print clarifai_data[z]


                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')

def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')

def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid\
                    ():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')

#Session Validation
def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
        time_to_live = session.created_on + timedelta(days=1)
        if time_to_live > timezone.now():
      return session.user
  else:
    return None


