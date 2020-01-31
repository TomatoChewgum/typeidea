from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

import xadmin
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager      # 使用xadmin 自定义过滤容器
from xadmin.filters import RelatedFieldListFilter
# Register your models here.
from .models import Post,Category,Tag
from .adminforms import PostAdminForm


from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline): # 可以选择继承 admin.TabularInline  admin.StackedInline
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 0 # 控制额外显示几个
    model = Post

@xadmin.sites.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name','status','is_nav','created_time','post_count')
#     fields = ('name','status','is_nav')
#
#     inlines = [PostInline, ]
#
#     """重写 ModelAdrnin 的 save_model 方法"""
#     def save_model(self, request, obj, form, change):
#         obj.owner = request.user
#         return super(CategoryAdmin, self).save_model(request,obj,form,change)
#
#     """ 自定义函数 """
#     def post_count(self,obj):
#         return obj.post_set.count()
#     post_count.short_description = '文章数量'

class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav')

    # inlines = [PostInline, ]

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'



@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')



""" 自定义过滤器类 """
class CategoryOwnerFilter(RelatedFieldListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    # title = '分类过滤器'
    # parameter_name = 'owner_category' # 查询时 URL 参数的名字

    @classmethod  # test 方法的作用是确认字段是否需要被当前的过滤器处理
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取 lookup_choices, 根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

    # """ 返回要展示的内容和查询的id """
    # def lookups(self, request, model_admin):
    #     return Category.objects.filter(owner=request.user).values_list('id','name')
    #
    # def queryset(self, request, queryset):
    #     category_id = self.value()
    #     if category_id:
    #         return queryset.filter(category_id=self.value())
    #     return queryset
manager.register(CategoryOwnerFilter, take_priority=True)

@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form =PostAdminForm
    list_display = ['title','category','status',
                    'created_time','owner','operator']
    list_display_links = []

    # list_filter = ['category', ]  # 根据 分类 进行过滤; 过滤器部分
    # list_filter =[CategoryOwnerFilter, ]
    list_filter = ['category', ] # 字段名
    search_fields = ['title','category_name']

    # actions_on_top = True
    # actions_on_bottom = True
    #
    # #form = PostAdminForm

    # 编辑页面
    # save_on_top = True
    # exclude = ('owner',)

    # fields =(
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    form_layout =(
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        ),
    )
    # @property
    # def media(self):
    #     # xadmin 基于 Bootstrap ,引入会导致页面样式冲突，这里只做演示
    #     media = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #     'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     })
    #     return media
    """ 自定义函数 """
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id,))
            # reverse('cus_admin:blog_post_change', args=(obj.id,)) # 获取 post对象的URL
            reverse('xadmin:blog_post_change', args=(obj.id,))
            #self.model_admin_url('change', obj.id)
        )

    operator.short_description = "操作"



    # class Media:
    #     css = {
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)


# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user',
#                     'change_message']



