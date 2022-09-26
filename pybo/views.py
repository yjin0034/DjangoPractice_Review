# 장고 뷰
# 장고에서 뷰는 어떤 데이터를 표시할지 정의하며, HTTP 응답 상태 코드(response)를 반환한다.
# views.py 파일에 애플리케이션의 처리 논리를 정의한다.
# 사용자가 입력한 URL에 따라, 모델(Model)에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, 템플릿(Template)에 전달하는 역할을 한다.
# 장고의 뷰 파일(views.py)은 요청에 따른 처리 논리를 정의한다.
# 즉, 사용자가 요청하는 값(request)을 받아 모델과 템플릿을 중개하는 역할을 한다.


from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer


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
    # pk : 모델의 기본키(Primary Key)  # 해당 모델의 pk는 id이다.
    # get_object_or_404() : 존재하지 않는 데이터를 요청할 경우 404 페이지 출력
    # question : 질문 데이터
    question = get_object_or_404(Question, pk=question_id)
    # 질문 데이터를 딕셔너리로 저장
    context = {'question': question}
    # 관련 질문으로 얻은 question 데이터(context)를 템플릿 파일(pybo/question_detail.html)에 적용하여 HTML을 생성한 후 리턴
    return render(request, 'pybo/question_detail.html', context)

# 답변 등록 관련 함수
def answer_create(request, question_id):
    # 전달받은 id와 관련된 (Question의) 질문 데이터 얻기
    question = get_object_or_404(Question, pk=question_id)
    # 답변 등록 시 텍스트창에 입력한 내용은 answer_create 함수의 첫번째 매개변수인 request 객체를 통해 읽을 수 있다.
    # 즉, request.POST.get('content')로 텍스트창에 입력한 내용을 읽을 수 있다.
    # request.POST.get('content') : POST로 전송된 폼(form) 데이터 항목 중 content 값을 의미
    # 답변을 생성하기 위해 Answer 모델에 답변과 관련된 질문(question=question), (텍스트창에 입력된) 답변 내용(content=request.POST.get('content')), 작성 일시(create_date=timezone.now()) 속성을 넣어 저장함
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    # redirect 함수 : 페이지 이동을 위한 함수
    # 답변을 생성한 후 질문 상세 화면을 다시 보여주기 위해 redirect 함수를 사용  # pybo:detail 별칭에 해당하는 페이지로 이동
    # pybo:detail 별칭에 해당하는 URL은 question_id가 필요하므로 question.id를 인수로 전달
    return redirect('pybo:detail', question_id=question.id)