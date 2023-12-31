from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ('user', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        labels = {
            'content': '댓글 남기기'
        }

        