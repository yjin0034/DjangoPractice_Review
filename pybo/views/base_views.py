# 장고 뷰
# 장고에서 뷰는 어떤 데이터를 표시할지 정의하며, HTTP 응답 상태 코드(response)를 반환한다.
# views.py 파일에 애플리케이션의 처리 논리를 정의한다.
# 사용자가 입력한 URL에 따라, 모델(Model)에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, 템플릿(Template)에 전달하는 역할을 한다.
# 장고의 뷰 파일(views.py)은 요청에 따른 처리 논리를 정의한다.
# 즉, 사용자가 요청하는 값(request)을 받아 모델과 템플릿을 중개하는 역할을 한다.


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from ..models import Question


# index 페이지 관련 함수 뷰
# 매개변수 request는 HTTP 요청 객체
def index(request):
    # 페이지
    # GET 방식으로 호출된 URL에서 page 값을 가져올 때 사용 (ex. http://localhost:8000/pybo/?page=1)
    # page 값 없이 호출된 경우에는 디폴트로 1이라는 값이 설정되게 함 (ex. http://localhost:8000/pybo/)
    page = request.GET.get('page', '1')
    # Question의 질문 목록 데이터 얻기
    # question_list : 질문 목록 데이터
    # order_by : 조회 결과를 정렬하는 함수
    # order_by('-create_date') : 작성 일시를 역순으로 정렬  # - : 역방향
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # (질문 목록 데이터를) 페이지당 10개씩 보여주기
    # paginator를 이용하여 요청된 페이지(page)에 해당되는, 페이징 객체(page_obj)를 생성
    # 이렇게 하면 장고 내부적으로는 데이터 전체를 조회하지 않고, 해당 페이지의 데이터만 조회하도록 쿼리가 변경됨
    page_obj = paginator.get_page(page)
    # 질문 목록 데이터를 딕셔너리로 저장
    context = {'question_list': page_obj}  # question_list는 페이징 객체(page_obj)
    # 데이터({'question_list': page_obj})를 템플릿 파일(pybo/question_list.html)에 적용하여 HTML을 생성한 후 리턴
    # render 함수 : 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수
    return render(request, 'pybo/question_list.html', context)

# 질문 상세 페이지 관련 함수 뷰
# 매개변수 question_id에는 URL 매핑시 저장된 question_id가 전달
def detail(request, question_id):
    # (인자로 받은) pk(question_id, 질문 id) 값에 해당하는 질문 데이터 얻기. (models의 Question 모델로부터) 데이터를 가져온다.
    # pk : 모델의 기본키(Primary Key)  # 해당 모델의 pk는 id이다.
    # get_object_or_404() : 존재하지 않는 데이터를 요청할 경우 404 페이지 출력
    # question : 질문 데이터
    question = get_object_or_404(Question, pk=question_id)
    # 질문 데이터를 딕셔너리로 저장
    context = {'question': question}
    # 관련 질문으로 얻은 question 데이터({'question': question})를 템플릿 파일(pybo/question_detail.html)에 적용하여 HTML을 생성한 후 리턴
    return render(request, 'pybo/question_detail.html', context)