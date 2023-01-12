from django.forms import ModelForm
from .models import Post, Reply


class PostForm(ModelForm):
    """Форма объявления"""
    class Meta:
        model = Post
        # fields = ['author', 'category', 'title', 'text', 'image']
        fields = ['category', 'title', 'text', 'image']


class ReplyForm(ModelForm):
    """Форма отклика"""
    class Meta:
        model = Reply
        fields = ['text', 'author', 'post']
