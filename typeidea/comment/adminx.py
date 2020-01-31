from django.contrib import admin

import xadmin

# Register your models here.
from .models import Comment

# @xadmin.sites.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('target','nickname','content',
#                     'website','created_time')

@xadmin.sites.register(Comment)
class CommentAdmin:
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')