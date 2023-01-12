from django.contrib.auth import login
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import ListView
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import Post
from .models import OneTimeCode, User
from .forms import UserRegisterForm, CodeForm
from .utils import generate_code


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'users/user_posts.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(author_id=self.request.user.id)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST['username'])
            code = OneTimeCode.objects.create(code=generate_code(), user=user)
            print(code.code, code.user)

            send_mail(subject='Регистраиця на портале billboard.',
                      message=f'Регистраиця на портале billboard. Код подтверждения {code.code}',
                      from_email='billboard <matoko18@yandex.ru>',
                      recipient_list=[f'{user.email}'],
                      html_message=f'<h2>Привет! Спасибо за регистрацию на порртале billboard</h2>'
                                   f'<p> Для завершения регистрации и входа в портал введи код <b>{code.code}</b>'
                                   f' в открывшейся форме на сайте или по '
                                   f'<a href="http://127.0.0.1:8000/users/register_code/{user.username}">ссылке</a></p>',
                      fail_silently=True)

            messages.success(request, 'Для завершения регистрации введите код из письма,'
                                      ' отправленного на вашу электронную почту.')
            return HttpResponseRedirect(reverse('users:register_code', kwargs={'username': request.POST['username']}))
    else:
        form = UserRegisterForm()
    context = {'title': 'Регистрация', 'form': form}
    return render(request, 'users/register.html', context)


def register_code(request, username):
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=username)[0]
            if OneTimeCode.objects.filter(code=request.POST['code'], user=user).exists():
                code_object = OneTimeCode.objects.get(code=request.POST['code'], user=user)
                code_object.used = True
                code_object.save()

                user.is_active = True
                user.save()

                login(request, user)
                return HttpResponseRedirect(reverse('posts:index'))
            else:
                messages.error(request, 'Введен неверный код.')
    else:
        form = CodeForm(request.POST)
    context = {'title': 'Регистрация', 'form': form}
    return render(request, 'users/register_with_code.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('posts:index'))
