from django.forms import ModelForm
from .models import Post, Reply, Category
from django import forms


class PostForm(ModelForm):
    """Форма объявления"""

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, widget=forms.widgets.Select(attrs={
        'class': 'post_category'}))

    class Meta:
        model = Post
        fields = ['category', 'title', 'text', 'image']


class ReplyForm(ModelForm):
    """Форма отклика"""
    class Meta:
        model = Reply
        fields = ['text', 'author', 'post']
