# 장고 URL
# 장고에서 URL은 URL 경로와 일치하는 뷰(View)를 매핑(Mapping)하거나 라우팅(Routing)하는 역할을 한다.
# 즉, 장고에서 URL 설정은 하나의 항목을 연결하는 퍼머링크(Permalink)를 생성하거나 쿼리스트링(Query string) 등을 정의할 수 있다.
# urls.py 파일에 URL 경로에 관한 논리를 정의한다.


from django.urls import path

from . import views


urlpatterns = [
    # path('') : '' 이 사용되었다. 이렇게 되는 이유는 config/urls.py 파일에서 이미 pybo/로 시작하는 URL이 pybo/urls.py 파일과 먼저 매핑되었기 때문
    path('', views.index),
]