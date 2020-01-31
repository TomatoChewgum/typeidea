from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'allways'
    priority = 1.0
    protocal = 'https'

    def items(self):  # 获取所有正常文章
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj): # 返回文章的最近更新时间
        return obj.created_time

    def location(self, obj): # 返回每篇文章的 url
        return reverse('post-detail', args=[obj.pk])
