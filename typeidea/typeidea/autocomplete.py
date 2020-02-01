from dal import autocomplete

from blog.models import Category, Tag

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        """ 判断用户是否登录 """
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)

        if self.q: # q 为url参数上传递过来的值
            qs = qs.filter(name__istartswith=self.q)

        return qs



class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        """ 判断用户是否登录 """
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.filter(owner=self.request.user)

        if self.q: # q 为url参数上传递过来的值
            qs = qs.filter(name__istartswith=self.q)

        return qs
