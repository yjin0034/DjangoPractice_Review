from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'common'

urlpatterns = [
    # 로그인 기능 URL 매핑
    # 로그인 뷰는, 따로 만들 필요 없이 django.contrib.auth 앱의 LoginView를 사용
    # template_name='common/login.html' : LoginView가 common 디렉터리의 템플릿을 참조하도록 설정
    # 본래, LoginView는 registration이라는 템플릿 디렉터리에서 login.html 파일을 찾는다. 그래서, registration/login.html과 같이 템플릿 파일을 작성해야 한다.
    # 하지만, 우리는 로그인을 common 앱에 구현할 것이므로 common 디렉터리에 템플릿을 생성할 것임.
    # 이를 위해 LoginView가 common 디렉터리의 템플릿을 참조할 수 있도록 template_name='common/login.html' 과 같이 설정.
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # 로그아웃 기능 URL 매핑
    # 로그아웃 뷰는 따로 만들 필요 없이, django.contrib.auth 앱의 LogoutView를 사용
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 회원가입 페이지 URL 매핑
    path('signup/', views.signup, name='signup'),
]