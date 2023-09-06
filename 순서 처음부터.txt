사진 업로드 등

python -m venv venv
source venv/Scripts/activate
pip install django
django-admin startproject insta .
django-admin startapp posts

@ settings.py
 posts 추가, BASE_DIR / 'templates'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

@ 최상위폴더 templates 폴더 내 base.html

pip install Pillow
pip freeze >> requirements.txt

@ (posts) models.py
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='image/%Y/%m')

python manage.py makemigrations
python manage.py migrate

@ (posts) admin.py
from .models import Post

admin.site.register(Post)

@ (insta) urls.py / from django.urls import path, include
    path('posts/', include('posts.urls')),

@ (posts) urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),

@ base.html
head 끝나기 전
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">

<body>

{% include '_nav.html' %}

  <div class="container">
    {% block body %}
    {% endblock %}

  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script>
</body>

@ temaplates 폴더 내 _nav.html 파일 생성
@ views.py 
from .models import Post

def index(request):
    posts = Post.objects.all()
    context= {
        'posts': posts,
    }
    return render(request, 'index.html', context)

@ posts 내 templates폴더 내 index.html 생성
{% extends 'base.html' %}

{% block body %}

    {{posts}}

{% endblock %}

@ _card.html 생성
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
######<!-- <h5 class="card-title">Card title</h5> -->
    <p class="card-text">{{post.content}}</p>
    <p>{{post.image}}</p>
    <p>{{post.image.url}}</p>
#####<!-- <a href="#" class="btn btn-primary">Go somewhere</a> -->
  </div>
</div>

( 업로드 후 확인은 posts)


@ (insta) urls.py
from django.conf import settings
from django.conf.urls.static import static

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

@ _card.html
<img src="{{post.image.url}}"
 {{post.content}} 외 주석

@ _nav.html
    <a class="navbar-brand" href="{% url 'posts:index' %}">Home</a>
        <a class="nav-link" href="{% url 'posts:create' %}">Create</a>

@ urls.py
    path('create/', views.create, name='create'),


@ views.py
def create(request):
    if request.method == 'POST':
        pass
    else:
        pass

@ (posts) forms.py 생성
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

@ views.py
from .forms import PostForm

    else:
        form = PostForm()
    
    context = {
        'form': form,
    }

    return render(request, 'form.html', context)

@ (templates) form.html 생성
{% extends 'base.html' %}

{% block body %}
  <form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form}}
    <input type="submit">
  </form>

{% endblock %}

@ views.py
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')

@ _card.html
# 업로드 경과 시간 표시
    <p class="card-text">{{post.created_at|timesince}}</p>

@ views.py
# 최신 게시물부터 출력
ef index(request):
    posts = Post.objects.all().order_by('-id')

# 사진 크기 조절 프로그램
pip install django-resized
pip freeze >> requirements.txt 

@ models.py
from django_resized import ResizedImageField
###### image = models.ImageField(upload_to='image/%Y/%m') #####
image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='image/%Y/%m'
    )

python manage.py makemigrations
python manage.py migrate



# 계정 설정
django-admin startapp accounts
 @ settings.py 'accounts'
(insta) urls.py /     path('accounts/', include('accounts.urls'))

@ (accounts) urls.py 생성
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]

@ (accounts) views.py
from django.shortcuts import render

def signup(request):
    if request.method == 'POST':
        pass
    else:
        pass

@ (accounts) models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

class User(AbstractUser):
    profile_image = ResizedImageField(
    size=[500, 500],
    crop=['middle', 'center'],
    upload_to='profile'
    )

@ settings.py / AUTH_USER_MODEL = 'accounts.User' 추가

# 새로운 user추가 했기 때문에 DB초기화하기
db.sqlite 삭제
migrations폴더들 내 0001삭제
python manage.py makemigrations
python manage.py migrate



@ (posts) models.py
from django.conf import settings
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

migrations폴더들 내 0001삭제
db.sqlite 삭제
python manage.py makemigrations
python manage.py migrate

@ (accounts) forms.py 생성
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        # model = User # 유지보수 번거로움
        fields = ('username', 'profile_image', )

@ (accounts) views.py
from django.shortcuts import render
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    
    return render(request, 'form.html', context)
# accounts - templates폴더 - accounts폴더 - form.html 생성
# 'form.html' -> 'accounts/form.html'

@ accounts - templates - accounts - form.html
{% extends 'base.html' %}

{% block body %}
<h1>Signup</h1>
<form action="" method="POST">
  {% csrf_token %}
  {{form}}
  <input type="submit">
</form>
{% endblock %}



pip install django-bootstrap-v5
pip freeze >> requirements.txt
 settings.py / "bootstrap5",

@ form.html
{% extends 'base.html' %}
{% load bootstrap5 %}

{% block body %}
<h1>Signup</h1>
<form action="" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {% bootstrap_form form %}
  <input type="submit">
</form>
{% endblock %}


	# 로그인 기능
@ (accounts) views.py
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')

@ (posts) _nav.html
        <a class="nav-link" href="{% url 'posts:create' %}">Create</a>
       <a class="nav-link" href="{% url 'accounts:signup' %}">Signup</a>
       <a class="nav-link" href="{% url 'accounts:login' %}">Login</a>

@ (accounts) urls.py
path('login/', views.login, name='login'),

@ views.py
def login(request):
    if request.method == 'POST':
        pass
    else:
        pass

@ forms.py
class CustomAuthenticationForm(AuthenticationForm):
    pass
@ views.py / from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')

@ _nav.html
{% if user.is_authenticated %}
        <a class="nav-link" href="{% url 'posts:create' %}">Create</a>
        <a class="nav-link" href="{% url 'accounts:signup' %}">Signup</a>
        {% else %}
        <a class="nav-link" href="{% url 'accounts:login' %}">Login</a>
        <a class="nav-link disabled" aria-disabled="true">{{request.user}}</a>
        {% endif %}

@ (posts) forms.py
# fields = '__all__'
        exclude = ('user', )

# 로그인한 유저 게시물 작성
@ (posts) views.py
if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

@ (posts - templates) _card.html
<div class="card mt-4">
  <div class="card-header">
    <p>
      <img src="{{post.user.profile_image.url}}" alt="" class="rounded-circle" width="50px">
      {{post.user}}
    </p>
  </div>

  <img src="{{post.image.url}}" alt="...">
.....

@ (accounts) urls.py
    path('<str:username>/', views.profile, name='profile'),

@ views.py
from django.contrib.auth import get_user_model

def profile(request, username):
    User = get_user_model()
    
    user_info = User.objects.get(username=username)

    context = {
        'user_info': user_info,
    }

    return render(request, 'accounts/profile.html', context)

@ accounts - templates - accounts - profile.html 생성

{% extends 'base.html' %}
{% block body %}
<div class="row">

  <div class="col-4">
    <img src="{{user_info.profile_image.url}}" alt="" class="img-fluid rounded-circle">
  </div>
  <div class="col-8">
    <div class="row">
      <div class="col-4">{{user_info.username}}</div>
      <div class="col-4"><a href="">팔로우</a></div>
    </div>
    <div class="row">
      <div class="col">게시물</div>
      <div class="col">팔로잉</div>
      <div class="col">팔로우</div>
    </div>
  </div>
</div>

<div class="row row-cols-3">
  {% for post in user_info.post_set.all %}
    <div class="col">
        <div class="card">
          <img src="{{post.image.url}}" alt="">
      </div>
    </div>
  {% endfor %}

</div>
{% endblock %}

	# 유저 누르면 작성글로 이동
@ _card.html
      <a href="{% url 'accounts:profile' username=post.user %}" class="text-reset text-decoration-none">{{post.user}}</a>

@ _nav.html
   <a href="{% url 'accounts:profile' username=user %}">{{user}}</a>

######<!-- <a class="nav-link disabled" aria-disabled="true">{{request.user}}</a> -->



























