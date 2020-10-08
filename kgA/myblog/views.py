from django.shortcuts import render

# Create your views here.
from django.views import View

from myblog.models import Blog, Category, Tag

from pure_pagination import PageNotAnInteger, Paginator

class IndexView(View):
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blog, 3, request=request)  #5为每页展示的数目
        all_blog=p.page(page)
        return render(request, 'index.html', {
            'all_blog': all_blog,
        })
class ArichiveView(View):

    def get(self, request):
        all_blog = Blog.objects.all().order_by('-create_time')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 4
        p = Paginator(all_blog, 1, request=request)
        all_blog = p.page(page)

        return render(request, 'archive.html', {
            'all_blog': all_blog,
        })