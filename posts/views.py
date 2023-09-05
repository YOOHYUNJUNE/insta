from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def index(request):
    posts = Post.objects.all().order_by('-id')
    comment_form = CommentForm()
    context= {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }

    return render(request, 'form.html', context)

@login_required
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False) # 작성하고 저장 전까지만 진행
        comment.user = request.user # 현재 로그인한 유저
        post = Post.objects.get(id=post_id) # post_id를 기준으로 찾은 post
        comment.post = post
        comment.save()

        return redirect('posts:index')
    
@login_required
def like(request, post_id):
    # 좋아요 버튼 누른 유저
    user = request.user
    post = Post.objects.get(id=post_id)

    # 이미 좋아요 -> 좋아요 취소
    if post in user.like_posts.all(): # 유저 기준
    # if post in user.like_posts.all(): 게시물 기준
        post.like_users.remove(user)
    
    # 좋아요 아직 안 누른 경우
    else:
        post.like_users.add(user)

    return redirect('posts:index')

def like_async(request, post_id):
    # context = {
    #     'message': post_id,
    # }
    user = request.user
    post = Post.objects.get(id=post_id)
    
    if user in post.like_users.all(): # 이미 좋아요
        post.like_users.remove(user)
        status = False
    else:   # 아직 좋아요X
        post.like_users.add(user)
        status = True
    context = {
        'status': status,
        'count': len(post.like_users.all())
    }
    return JsonResponse(context)




