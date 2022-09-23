# 장고 뷰
# 장고에서 뷰는 어떤 데이터를 표시할지 정의하며, HTTP 응답 상태 코드(response)를 반환한다.
# views.py 파일에 애플리케이션의 처리 논리를 정의한다.
# 사용자가 입력한 URL에 따라, 모델(Model)에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, 템플릿(Template)에 전달하는 역할을 한다.
# 장고의 뷰 파일(views.py)은 요청에 따른 처리 논리를 정의한다.
# 즉, 사용자가 요청하는 값(request)을 받아 모델과 템플릿을 중개하는 역할을 한다.


from django.shortcuts import render
from .models import Question

# index 페이지 관련 함수
# 매개변수 request는 HTTP 요청 객체
def index(request):
    # Question의 질문 목록 데이터 얻기
    # question_list : 질문 목록 데이터
    # order_by : 조회 결과를 정렬하는 함수
    # order_by('-create_date') : 작성 일시를 역순으로 정렬  # - : 역방향
    question_list = Question.objects.order_by('-create_date')
    # 질문 목록 데이터를 딕셔너리로 저장
    context = {'question_list': question_list}
    # 질문 목록으로 조회한 question_list 데이터(context)를 템플릿 파일(pybo/question_list.html)에 적용하여 HTML을 생성한 후 리턴
    # render 함수 : 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
    return render(request, 'pybo/question_list.html', context)

# 질문 상세 페이지 관련 함수
# 매개변수 question_id에는 URL 매핑시 저장된 question_id가 전달
def detail(request, question_id):
    # 전달받은 id와 관련된 (Question의) 질문 데이터 얻기
    # question : 질문 데이터
    question = Question.objects.get(id=question_id)
    # 질문 데이터를 딕셔너리로 저장
    context = {'question': question}
    # 관련 질문으로 얻은 question 데이터(context)를 템플릿 파일(pybo/question_detail.html)에 적용하여 HTML을 생성한 후 리턴
    return render(request, 'pybo/question_detail.html', context)


