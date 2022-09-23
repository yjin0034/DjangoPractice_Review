# 장고 URL
# 장고에서 URL은 URL 경로와 일치하는 뷰(View)를 매핑(Mapping)하거나 라우팅(Routing)하는 역할을 한다.
# 즉, 장고에서 URL 설정은 하나의 항목을 연결하는 퍼머링크(Permalink)를 생성하거나 쿼리스트링(Query string) 등을 정의할 수 있다.
# urls.py 파일에 URL 경로에 관한 논리를 정의한다.


from django.urls import path

from . import views


# URL 네임스페이스 설정
app_name = 'pybo'

urlpatterns = [
    # index 페이지 URL 매핑
    # path('') : '' 이 사용되었다. 이렇게 되는 이유는 config/urls.py 파일에서 이미 pybo/로 시작하는 URL이 pybo/urls.py 파일과 먼저 매핑되었기 때문
    # name='index' : 해당 URL에 대해 URL 별칭 설정
    path('', views.index, name='index'),
    # 질문 상세 페이지 URL 매핑
    # <int:question_id> : 정수형 숫자 매핑
    # 예를 들어, 만일 http://localhost:8000/pybo/2/ 페이지가 요청되면
    # 여기에 등록한 매핑 룰에 의해 http://localhost:8000/pybo/<int:question_id>/ 가 적용되어,
    # question_id 에 2가 저장되고, views.detail 함수도 실행.
    # name='detail' : 해당 URL에 대해 URL 별칭 설정
    path('<int:question_id>/', views.detail, name='detail'),
    # 답변 등록 기능 URL 매핑
    # 예를 들어, 만일 http://locahost:8000/pybo/answer/create/2/ 페이지가 요청되면
    # 여기에 등록한 매핑 룰에 의해 http://localhost:8000/pybo/answer/create/<int:question_id>/ 가 적용되어,
    # question_id 에 2가 저장되고, views.answer_create 함수도 실행.
    # name='answer_create' : 해당 URL에 대해 URL 별칭 설정
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
]