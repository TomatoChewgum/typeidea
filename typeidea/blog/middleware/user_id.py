import uuid

USER_KEY = 'uid'
TEN_YEARS = 60*60*24*356*10

"""
middleware逻辑： Django middleware 在项目启动时会被初始化，等接受请求之后，
会根据settings 中的 MIDDLEWARE 配置的顺序挨个调用，传递request作为参数。

UserIDMiddleware 逻辑：在接受请求之后，先生成uid，然后把uid赋值给request对象。
因为request是一个类的实例，可以动态赋值。因此，我们动态给其添 uid 属性， 这样在后面的
View中就可以拿到 uid并使用了。最后返回 response 时，我们设置 cookie，并且设置为httponly（即
只在服务端能访问） 这样用户再次请求时， 就会带上同样的 uid 信息了
"""
class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid



