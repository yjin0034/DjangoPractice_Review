# 장고 뷰
# 장고에서 뷰는 어떤 데이터를 표시할지 정의하며, HTTP 응답 상태 코드(response)를 반환한다.
# views.py 파일에 애플리케이션의 처리 논리를 정의한다.
# 사용자가 입력한 URL에 따라, 모델(Model)에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, 템플릿(Template)에 전달하는 역할을 한다.
# 장고의 뷰 파일(views.py)은 요청에 따른 처리 논리를 정의한다.
# 즉, 사용자가 요청하는 값(request)을 받아 모델과 템플릿을 중개하는 역할을 한다.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


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

# 질문 등록 관련 함수 뷰
@login_required(login_url='common:login')
def question_create(request):
    # POST 요청 방식
    # 질문 등록 페이지에서 subject, content 항목에 값을 기입하고 '저장하기' 버튼을 누르면 /pybo/question/create/ 페이지를 POST 방식으로 요청한다.
    # (question_form.html의) form 태그에 action 속성을 지정하지 않아 현재 페이지가 디폴트 action으로 설정되기 때문
    if request.method == 'POST':
        # (pybo/forms의) QuestionForm으로부터 폼 데이터를 전달받음
        # request.POST에는 화면에서 사용자가 입력한 내용들이 담겨있다.
        form = QuestionForm(request.POST)  # request.POST를 인수로 QuestionForm을 생성할 경우, request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        # form.is_valid() : form이 유효한지를 검사  # 만약 form에 저장된 subject, content의 값이 올바르지 않다면 form에는 오류 메시지가 저장
        if form.is_valid():  # 폼이 유효하다면,
            # form에 저장된 데이터로 Question 데이터를 저장하기 위한 코드  # QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 이와 같이 사용할 수 있음
            # commit=False : 임시 저장. 즉, 실제 데이터는 아직 데이터베이스에 저장되지 않은 상태
            # 여기서, form.save(commit=False) 대신 form.save()를 수행하면 Question 모델의 create_date에 값이 없다는 오류가 발생할 것이다.
            # 왜냐하면, QuestionForm에는 현재 subject, content 속성만 정의되어 있고 create_date 속성은 없기 때문이다. 이러한 이유로 임시 저장을 먼저 하여 question 객체를 리턴받고 create_date에 값을 설정한 후 question.save()로 실제 데이터를 저장하는 것
            # (create_date 속성은 데이터 저장 시점에 생성해야 하는 값이므로 QuestionForm에 등록하여 사용하지 않는다.)
            question = form.save(commit=False)  # 임시 저장하여 question 객체를 리턴받는다.
            # 질문의 작성자
            # author 속성에 로그인 계정 저장  # request.user : 현재 로그인한 계정의 User 모델 객체
            question.author = request.user
            question.create_date = timezone.now()  # 실제 저장을 위해, 작성 일시를 설정
            question.save()  # 데이터를 실제로 저장
            return redirect('pybo:index')
    # GET 요청 방식
    # 질문 목록 화면에서 질문 '등록하기' 버튼을 클릭한 경우, /pybo/question/create/ 페이지가 GET 방식으로 요청되어 question_create 함수가 실행
    else:
        # (pybo/forms의) QuestionForm으로부터 폼 데이터를 전달받음
        form = QuestionForm()
    context = {'form': form}  # {'form': form}은 관련 템플릿에서 질문 등록 시 사용할 폼 엘리먼트를 생성할 때 쓰일 것이다
    # 폼 데이터({'form': form})를 템플릿 파일(pybo/question_form.html)에 적용하여 HTML을 생성한 후 리턴
    return render(request, 'pybo/question_form.html', context)

# 질문 수정 관련 함수 뷰
@login_required(login_url='common:login')
def question_modify(request, question_id):
    # (인자로 받은) 질문 id(question_id)에 해당하는 질문 데이터 얻기. (models의 Question 모델로부터) 데이터를 가져온다.
    question = get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자와 수정하려는 질문의 작성자가 다를 경우에는, "수정권한이 없습니다"라는 오류를 발생
    if request.user != question.author:
        # messages 모듈 : 장고가 제공하는 모듈로 넌필드 오류(non-field error)를 발생시킬 경우에 사용
        messages.error(request, '수정 권한이 없습니다')
        # 오류 발생 후 질문 상세 화면으로 이동  # pybo:detail 별칭에 해당하는 페이지로 이동
        # pybo:detail 별칭에 해당하는 URL은 question_id가 필요하므로 question.id를 인수로 전달
        return redirect('pybo:detail', question_id)
    # POST 요청 방식
    # 동작 예) 질문 수정 화면에서 "저장하기" 버튼을 클릭하면, http://localhost:8000/pybo/question/modify/2/ 페이지가 POST 방식으로 호출되어 데이터가 수정됨
    if request.method == "POST":
        # QuestionForm(request.POST, instance=question) : instance를 기준으로 QuestionForm을 생성하지만, request.POST의 값으로 덮어쓰라는 의미
        # 따라서 질문 수정 화면에서 제목 또는 내용을 변경하여 POST 요청하면, 변경된 내용이 QuestionForm에 저장될 것.
        # request.POST에는 화면에서 사용자가 입력한 내용들이 담겨있다.
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정 일시 저장  # 수정 일시는 현재 일시로 지정
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    # GET 요청 방식
    # 동작 예) 질문 상세 화면에서 "수정" 버튼을 클릭하면, http://localhost:8000/pybo/question/modify/2/ 페이지가 GET 방식으로 호출되어 질문 수정 화면이 보여짐
    else:
        # 폼 생성시 이처럼 instance 값을 지정하면, 폼의 속성 값이 instance의 값으로 채워진다. 따라서 질문을 수정하는 화면에서 제목과 내용이 채워진 채로 보이게 됨.
        # 질문 수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록 다음과 같이 폼을 생성
        form = QuestionForm(instance=question)
    context = {'form': form}
    # 폼 데이터({'form': form})를 템플릿 파일(pybo/question_form.html)에 적용하여 HTML을 생성한 후 리턴
    return render(request, 'pybo/question_form.html', context)

# 질문 삭제 관련 함수 뷰
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자와 삭제하려는 질문의 글쓴이가 다를 경우에는, "삭제 권한이 없습니다"라는 오류를 발생
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다')
        # 질문 상세 페이지로 다시 이동
        return redirect('pybo:detail', question_id=question.id)
    else:
        # 해당 질문 삭제
        question.delete()
        # 삭제 후, index 페이지로 이동
    return redirect('pybo:index')

# 답변 등록 관련 함수 뷰
# answer_create 뷰는 함수 내에서 request.user를 사용하므로 로그인이 필요한 함수이다. 따라서, 아래와 같이 @login_requred 어노테이션을 사용해야 한다.
# @login_required 어노테이션이 붙은 함수 : 로그인이 필요한 함수를 의미
# @login_required 어노테이션은 login_url='common:login' 처럼 이동할 로그인 화면 URL을 지정할 수 있다.
# 로그아웃 상태에서 @login_required 어노테이션이 적용된 함수가 호출되면 자동으로 로그인 화면(login_url='common:login')으로 이동하게 됨
@login_required(login_url='common:login')
def answer_create(request, question_id):
    # (인자로 받은) 질문 id(question_id)에 해당하는 질문 데이터 얻기. (models의 Question 모델로부터) 데이터를 가져온다.
    question = get_object_or_404(Question, pk=question_id)
    # POST 요청 방식
    if request.method == "POST":
        # (pybo/forms의) AnswerForm으로부터 폼 데이터를 전달받음
        # request.POST에는 화면에서 사용자가 입력한 내용들이 담겨있다.
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            # 답변의 작성자
            # author 속성에 로그인 계정 저장  # request.user : 현재 로그인한 계정의 User 모델 객체
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # redirect 함수 : 페이지 이동을 위한 함수
            # 답변을 생성한 후 질문 상세 화면을 다시 보여주기 위해 redirect 함수를 사용  # pybo:detail 별칭에 해당하는 페이지로 이동
            # pybo:detail 별칭에 해당하는 URL은 question_id가 필요하므로 question.id를 인수로 전달
            return redirect('pybo:detail', question_id=question.id)
    # GET 요청 방식
    else:
        # 바로 이전 코드 때에는, 로그인되어 있지 않은 상태에서, "답변등록" 버튼을 누르고 로그인 화면으로 이동해 로그인을 수행하면 405 오류가 발생한다.
        # 답변 등록 시 POST가 아닌 경우 HttpResponseNotAllowed 오류를 발생시키도록 코딩했었기 때문에.
        # 이전 코드 : return HttpResponseNotAllowed('Only POST is possible')
        # 하지만, 아래 코드로 바꿔주면 이제 로그아웃 상태에서 "답변등록" 버튼을 누르더라도 로그인 수행 후 405 오류가 발생하지 않고 다시 질문 상세화면으로 잘 돌아간다.
        # 수정 코드 : form = AnswerForm()
        # (pybo/forms의) AnswerForm으로부터 폼 데이터를 전달받음
        form = AnswerForm()
    context = {'question': question, 'form': form}
    # 질문 데이터({'question': question})와 폼 데이터({'form': form})를 템플릿 파일(pybo/question_detail.html)에 적용하여 HTML을 생성한 후 리턴
    return render(request, 'pybo/question_detail.html', context)

# 답변 수정 관련 함수 뷰
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # (인자로 받은) pk(answer_id, 답변 id) 값에 해당하는 답변 데이터 얻기. (models의 Answer 모델로부터) 데이터를 가져온다.
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다')
        # 오류 발생 후 질문 상세 화면으로 이동  # pybo:detail 별칭에 해당하는 페이지로 이동
        # pybo:detail 별칭에 해당하는 URL은 question_id가 필요하므로 answer.question.id를 인수로 전달
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    # 답변 데이터({'answer': answer})와 폼 데이터({'form': form})를 템플릿 파일(pybo/answer_form.html)에 적용하여 HTML을 생성한 후 리턴
    return render(request, 'pybo/answer_form.html', context)

# 답변 삭제 관련 함수 뷰
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)