from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
    ReplyCreateView, accept_reply, delete_reply

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('posts/add/', PostCreateView.as_view(), name='add_post'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='update_post'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('posts/<int:pk>/reply/add', ReplyCreateView.as_view(), name='add_reply'),
    path('reply/<int:pk>/accept', accept_reply, name='accept_reply'),
    path('reply/<int:pk>/delete', delete_reply, name='delete_reply'),
]
