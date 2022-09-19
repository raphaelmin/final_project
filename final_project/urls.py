from django.contrib import admin
from django.urls import path

from user.views import index, login_view, logout_view, register_view, user_list_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", index, name="index"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("users/", user_list_view, name="user_list"),

# index 페이지의 경로가 / 인지 /index/ 인지 명확하지 않아서 명칭은 index 이지만 경로는 / 인 것을 기준으로 하였습니다.

]
