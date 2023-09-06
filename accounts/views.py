from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # 회원가입시 바로 로그인
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)

# accounts의 signup.html이 없는데도 signup 페이지가 존재하는 이유
    # settings.py의 TEMPLATES가 모든 파일들을 순회하며 .html파일을 따로 저장,
    # 거기에 있는 posts의 form.html을 그대로 사용 (동일 이름시 먼저 만든 파일 적용)

    # accounts - templates폴더 - accounts폴더 - form.html

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')
    else:
        form = CustomAuthenticationForm
    
    context = {
        'form': form,
    }

    return render(request, 'accounts/login.html', context)

def profile(request, username):
    User = get_user_model()
    
    user_info = User.objects.get(username=username)

    context = {
        'user_info': user_info,
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, username):
    User = get_user_model()

    me = request.user # 현재 로그인한 유저
    you = User.objects.get(username=username) # 내가 팔로우 하려는 사람
    
    # 팔로잉 이미 되어 있는 경우
    if you in me.followings.all():
        me.followings.remove(you)
    
    # 팔로잉 아직 안 된 경우
    else:
        me.followings.add(you)

    return redirect('accounts:profile', username=username)



def logout(request):
    auth_logout(request)
    return redirect('accounts:login')



