# 장고 뷰
# 장고에서 뷰는 어떤 데이터를 표시할지 정의하며, HTTP 응답 상태 코드(response)를 반환한다.
# views.py 파일에 애플리케이션의 처리 논리를 정의한다.
# 사용자가 입력한 URL에 따라, 모델(Model)에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, 템플릿(Template)에 전달하는 역할을 한다.
# 장고의 뷰 파일(views.py)은 요청에 따른 처리 논리를 정의한다.
# 즉, 사용자가 요청하는 값(request)을 받아 모델과 템플릿을 중개하는 역할을 한다.


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question


# index 페이지 관련 함수 뷰
# 매개변수 request는 HTTP 요청 객체
def index(request):
    # 페이지
    # GET 방식으로 호출된 URL에서 page 값을 가져올 때 사용 (ex. http://localhost:8000/pybo/?page=1)
    # page 값 없이 호출된 경우에는 디폴트로 1이라는 값이 설정되게 함 (ex. http://localhost:8000/pybo/)
    page = request.GET.get('page', '1')
    # 검색어
    # 화면으로부터 전달받은 검색어
    kw = request.GET.get('kw', '')
    # Question의 질문 목록 데이터 얻기
    # question_list : 질문 목록 데이터
    # order_by : 조회 결과를 정렬하는 함수
    # order_by('-create_date') : 작성 일시를 역순으로 정렬  # - : 역방향
    question_list = Question.objects.order_by('-create_date')
    # Q 함수 : OR조건으로 데이터를 조회하기 위해 사용하는 함수. 제목, 내용, 글쓴이를 OR 조건으로 검색하기 위해 사용
    # distinct 함수 : 조회 결과에 중복이 있을 경우 중복을 제거하여 리턴하는 함수
    # 하나의 질문에는 여러 개의 답변이 있을 수 있는데, 이 때 여러 개의 답변이 검색 조건에 해당될 때 동일한 질문이 중복으로 조회될 수 있다. 이런 이유로 중복된 질문을 제거하기 위해 distinct를 사용
    # subject__icontains=kw : 제목에 kw 문자열이 포함되었는지를 확인
    # answer__author__username__icontains=kw : 답변을 작성한 사람의 이름에 kw 문자열이 포함되는지 확인
    # filter 함수에서 모델 속성에 접근하기 위해서는, 이처럼 __(언더바 두개)를 이용하여 하위 속성에 접근할 수 있다.
    # contains과 icontains의 차이점 : icontains를 사용하면 대소문자를 가리지 않고 찾아준다.
    if kw:  # kw(검색어)가 존재한다면,
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)  # (질문 목록 데이터를) 페이지당 10개씩 보여주기
    # paginator를 이용하여 요청된 페이지(page)에 해당되는, 페이징 객체(page_obj)를 생성
    # 이렇게 하면 장고 내부적으로는 데이터 전체를 조회하지 않고, 해당 페이지의 데이터만 조회하도록 쿼리가 변경됨
    page_obj = paginator.get_page(page)
    # 질문 목록 데이터와 page, kw를 딕셔너리로 저장
    # question_list : 질문 목록 데이터
    # question_list는 페이징 객체(page_obj)
    # context = {..., 'page': page, 'kw': kw} : page와 kw를 템플릿에 전달하기 위해 context 딕셔너리에 추가
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    # 데이터({'question_list': page_obj, 'page': page, 'kw': kw})를 템플릿 파일(pybo/question_list.html)에 적용하여 HTML을 생성한 후 리턴
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