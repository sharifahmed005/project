from django.urls import path

from blog.views import BlogDetailsView, BlogView, comments
urlpatterns = [
    path('blogs/', BlogView.as_view(), name='viewBlog'),
    path('blog-details/<pk>/', BlogDetailsView.as_view(), name='blog-details'),
    path('comment-post', comments, name='comment_post')
]
