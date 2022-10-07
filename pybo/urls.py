# 장고 URL
# 장고에서 URL은 URL 경로와 일치하는 뷰(View)를 매핑(Mapping)하거나 라우팅(Routing)하는 역할을 한다.
# 즉, 장고에서 URL 설정은 하나의 항목을 연결하는 퍼머링크(Permalink)를 생성하거나 쿼리스트링(Query string) 등을 정의할 수 있다.
# urls.py 파일에 URL 경로에 관한 논리를 정의한다.


from django.urls import path

from .views import base_views, question_views, answer_views


# URL 네임스페이스 설정
app_name = 'pybo'

urlpatterns = [
    # base_views.py
    #
    # index 페이지 URL 매핑
    # pybo/ 로 시작하는 페이지를 요청하면, (pybo/views의) base_views.index 함수 뷰를 호출하도록 함
    # path('') : '' 이 사용되었다. 이렇게 되는 이유는 config/urls.py 파일에서 이미 pybo/로 시작하는 URL이 pybo/urls.py 파일과 먼저 매핑되었기 때문
    # name='index' : 해당 URL에 대해 URL 별칭 설정
    path('', base_views.index, name='index'),
    # 질문 상세 페이지 URL 매핑
    # pybo/[정수형 숫자]로 시작하는 페이지를 요청하면, 해당 정수형 숫자를 question_id에 저장하고, base_views.detail 함수 뷰를 호출
    # <int: > : 정수형 숫자 매핑
    # 예를 들어, 만일 http://localhost:8000/pybo/2/ 페이지가 요청되면
    # 여기에 등록한 매핑 룰에 의해 http://localhost:8000/pybo/<int:question_id>/ 가 적용되어,
    # question_id 에 2가 저장되고, base_views.detail 함수 뷰도 실행.
    # name='detail' : 해당 URL에 대해 URL 별칭 설정
    path('<int:question_id>/', base_views.detail, name='detail'),

    # question_views.py
    #
    # 질문 등록 기능 URL 매핑
    # pybo/question/create로 시작하는 페이지를 요청하면, question_views.question_create 함수 뷰를 호출
    path('question/create/', question_views.question_create, name='question_create'),
    # 질문 수정 기능 URL 매핑
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    # 질문 삭제 기능 URL 매핑
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    # answer_views.py
    #
    # 답변 등록 기능 URL 매핑
    # pybo/answer/create/[정수형 숫자]로 시작하는 페이지를 요청하면, 해당 정수형 숫자를 question_id에 저장하고, answer_views.answer_create 함수 뷰를 호출
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    # 답변 수정 기능 URL 매핑
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    # 답변 삭제 기능 URL 매핑
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
]