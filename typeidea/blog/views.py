from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.

from django.http import HttpResponse
from django.views.generic import DetailView,ListView


from .models import  Post, Tag, Category
from config.models import SideBar


# def post_list(request, category_id=None, tag_id=None):
#     content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(
#         category_id = category_id, tag_id = tag_id
#     )
#
#     return HttpResponse(content)
#
# def post_detail(request, post_id):
#     return HttpResponse('detail')

# def post_list(request, category_id=None, tag_id=None):
#     return render(request, 'blog/list.html', context={'name':'post_list'})
#
# def post_detail(request, post_id=None):
#     return render(request, 'blog/detail.html', context={'name':'post_detail'})
#

# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         try:
#             tag = Tag.objects.get(id=tag_id)
#         except Tag.DoesNotExist:
#             post_list = []
#         else:
#             post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#     else:
#         post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             try:
#                 category = Category.objects.get(id=category_id)
#             except Category.DoseNotExist:
#                 category = None
#             else:
#                 post_list = post_list.filter(category_id=category_id)
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#     }
#
#    # return render(request, 'blog/list.html', context={'post_list':post_list})
#     return render(request, 'blog/list.html', context=context)
#
# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     return render(request, 'blog/detail.html', context={'post':post})



class CommonViewMixin:
    def get_context_data(self, **kwargs):
        # print("demo -----------")
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class CategoryView(IndexView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写 queryset ,根据分类过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

def tag_view(request, tag_id=None): # 函数形式
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs()) # 将  Category.get_navs() 返回的字典 添加到 context字典
    return render(request, 'blog/list.html', context=context)

class TagView(IndexView):
    """ 用来获取上下文数据－并最终将其传入模板 """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')  # self.kwargs 中的数据其实是从我们的 URL 定义中拿到的
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    """ 用来获取指定 Model 或者 QuerySet 的数据 """
    def get_queryset(self):
        """ 重写 queryset, 根据标签过滤 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id) # 此处注意是 tag__id 而不是 tag_id (目前不知道问题)


def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
        # post_list = Post.objects.filter(status=Post.STATUS_NORMAL)

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs()) # 将  Category.get_navs() 返回的字典 添加到 context字典

    # return render(request, 'blog/list.html', context={'post_list':post_list})
    return render(request, 'blog/list.html', context=context)

class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 5  # 把每页的数量设置为1
    context_object_name = 'post_list' # 如果不设置此项，在模板中需要使用object_list 变量
    template_name = 'blog/list.html'

def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)

""" 将 function view 改为 class-based view"""

class PostDetailView(CommonViewMixin, DetailView): # CommonViewMixin
    # model = Post
    # template_name = 'blog/detail.html'

    queryset = Post.latest_posts() # queryset 与 model 二选一，queryset可以进行对数据的过滤
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
