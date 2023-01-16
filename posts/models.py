from django.db import models

from users.models import User


class Category(models.Model):
    """Категории"""
    title = models.CharField(max_length=255, unique=True, verbose_name='название категории')

    def __str__(self):
        return self.title


class Post(models.Model):
    """Объявления"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст')
    image = models.ImageField(upload_to='posts_images', blank=True)

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'{self.title} - {self.author}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'


class Reply(models.Model):
    """ Отклики"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='объявление')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='текст')
    accept = models.BooleanField(default=False, verbose_name='принят')

    def __str__(self):
        return f'{self.text} - {self.post}'

    class Meta:
        ordering = ['-created_at']
