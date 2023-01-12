from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category, Reply
from .forms import PostForm, ReplyForm
from users.models import User


class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'posts/post_create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            return super().post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('users:login'))

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        print(self.object.author)
        print(request.user)
        if self.object.author == request.user:
            self.object.delete()
        return HttpResponseRedirect(success_url)

    def form_valid(self, form):
        pass


class ReplyCreateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        form = ReplyForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form.save()

            reply = Reply.objects.get(text=request.POST['text'], author=request.POST['author'])

            send_mail(subject=f'Новый отклик на объявление "{post.title}" на портале billboard.',
                      message=f'Новый отклик на объявление "{post.title}" на портале billboard.',
                      from_email='billboard <matoko18@yandex.ru>',
                      recipient_list=[f'{post.author.email}'],
                      html_message=f'<h2>Появился отклик на объявление "{post.title}"</h2>'
                                   f'<p> Отправил пользователь: <b>{reply.author}</b></p>'
                                   f'<p>"{request.POST["text"]}"</p>',
                      fail_silently=True)

        return redirect(post.get_absolute_url())


@login_required
def accept_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.accept = True
    reply.save()

    send_mail(subject=f'Принят ваш отклик на портале billboard.',
              message=f'Принят ваш отклик на портале billboard.',
              from_email='billboard <matoko18@yandex.ru>',
              recipient_list=[f'{reply.author.email}'],
              html_message=f'<h2>Ваш отклик на объявление "{reply.post.title}" принят</h2>',
              fail_silently=True)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
