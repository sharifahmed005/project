
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Blog, Comments
# Create your views here.


class BlogView(ListView):
    queryset = Blog.objects.all()
    context_object_name = 'blogs'


class BlogDetailsView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()
        context['comments'] = Comments.objects.filter(
            blog_id=self.kwargs['pk'])
        print(self.kwargs['pk'])
        return context


def comments(request):
    if request.method == 'POST':
        blog = request.POST['blog']
        comment = request.POST['comment']
        Comments.objects.create(
            blog_id=blog, comment=comment, commenter_id=request.user.id)
        return redirect('blog-details', blog)

    return HttpResponse('It Not Working')
