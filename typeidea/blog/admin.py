from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

# Register your models here.
from .models import Post,Category,Tag
from .adminforms import PostAdminForm


from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline): # 可以选择继承 admin.TabularInline  admin.StackedInline
    fields = ('title', 'desc')
    extra = 0 # 控制额外显示几个
    model = Post

@admin.register(Category,site=custom_site)
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

    inlines = [PostInline, ]

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'



@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')



""" 自定义过滤器类 """
class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = '分类过滤器'
    parameter_name = 'owner_category' # 查询时 URL 参数的名字

    """ 返回要展示的内容和查询的id """
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display = ['title','category','status',
                    'created_time','owner','operator']
    list_display_links = []

    # list_filter = ['category', ]  # 根据 分类 进行过滤; 过滤器部分
    list_filter =[CategoryOwnerFilter]
    search_fields = ['title','category_name']

    actions_on_top = True
    actions_on_bottom = True

    #form = PostAdminForm

    #编辑页面
    # save_on_top = True
    # exclude = ('owner',)

    # fields =(
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag', ),
        })
    )
    # filter_horizontal = ('tag',)
    filter_vertical = ('tag',)
    """ 自定义函数 """
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id,))
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = "操作"



    class Media:
        css = {
            'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']



