from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    user = request.user
    return render(request, "index.html", {"user": user})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요

        form = LoginForm(request.POST)
        if form.is_valid():
            # 뭔가 빠진 것 같은데...form에 입력된 데이터를 User로 가져와야 할 듯 한데...

            # TODO: 네 맞아요. form에 입력된 데이터를 User로 가져와야 합니다. 괜히 form을 써보라는 것이 아니니까요
            # form을 쓴다는 것에 힌트가 있어요!

            # is_valid() method를 사용하면 form에 입력된 데이터가 form.cleaned_data dictionary에 저장되네요. https://docs.djangoproject.com/en/4.1/topics/forms/

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # authenticate()와 login()을 사용하면 되네요. https://docs.djangoproject.com/en/4.1/topics/auth/default/
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            
            else:
                form = LoginForm()						          
            
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요						

    logout(request)
    
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요

# login_required decorator를 사용하면 되네요. https://docs.djangoproject.com/en/4.1/topics/auth/default/
@login_required(login_url='/login/')

def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요

    # Paginator()를 사용하면 되네요. https://docs.djangoproject.com/en/4.1/topics/pagination/
    user_list = User.objects.all()
    paginator = Paginator(user_list, 5)
    
    page_number = request.GET.get('page')
    # TODO: page가 없을 때의 default 값도 하나 있으면 좋을 것 같습니다.
    
    # HTTP GET parameters에 page 정보가 포함되어 있지 않은 경우에 page_number의 default 값을 1로 하였습니다.
    # request.GET.get('page')를 사용했는데 request는 HttpRequest object인 듯 합니다. 
    # HttpRequest.GET은 "A dictionary-like object containing all given HTTP GET parameters."라고 하네요. https://docs.djangoproject.com/en/4.1/ref/request-response/#django.http.QueryDict
    # 참고로, user 목록 최초 접속시에는 브라우저 주소창에 page 정보가 표시 표시되지 않는데 http://127.0.0.1:8000/users/, '이전으로' 또는 '다음으로' 버튼을 클릭하면 브라우저 주소창에 page 정보가 표시되네요. http://127.0.0.1:8000/users/?page=1
    if page_number is None:
        page_number = 1
   
    users = paginator.get_page(page_number)
    # page_number가 None인 경우에는 1로 보고 처리하는 것 같습니다.
 

    return render(request, "users.html", {"users": users})
