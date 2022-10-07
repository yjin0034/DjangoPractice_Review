"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# 장고 URL
# 장고에서 URL은 URL 경로와 일치하는 뷰(View)를 매핑(Mapping)하거나 라우팅(Routing)하는 역할을 한다.
# 즉, 장고에서 URL 설정은 하나의 항목을 연결하는 퍼머링크(Permalink)를 생성하거나 쿼리스트링(Query string) 등을 정의할 수 있다.
# urls.py 파일에 URL 경로에 관한 논리를 정의한다.


from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views


urlpatterns = [
    # admin/ 로 시작하는 페이지를 요청하면, admin.site.urls를 호출
    # 뒤에 /(슬래시)를 붙여주면 브라우저 주소창에 http://localhost:8000/pybo 라고 입력해도 자동으로 http://localhost:8000/pybo/ 처럼 변환된다. 이렇게 되는 이유는 URL을 정규화하는 장고의 기능 때문
    # 특별한 경우가 아니라면 URL 매핑시 항상 끝에 슬래시를 붙여 준다.
    path('admin/', admin.site.urls),
    # pybo/ 로 시작하는 페이지를 요청하면, pybo/urls.py 파일의 매핑 정보를 읽어서 처리하도록 함
    path('pybo/', include('pybo.urls')),
    # common/ 으로 시작하는 URL은 모두 common/urls.py 파일을 참조하게 함
    path('common/', include('common.urls')),
    # '/'에 해당되는 path
    # / 페이지 요청에 대해 아래의 해당 path('', views.index, name='index')가 작동하여 pybo/views.py 파일의 index 함수 뷰가 실행됨
    # 메인 페이지인 듯
    path('', base_views.index, name='index'),
]
