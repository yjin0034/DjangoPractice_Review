from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


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