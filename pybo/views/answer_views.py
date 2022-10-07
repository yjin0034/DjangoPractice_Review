from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


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
            # 답변을 생성(또는 수정, 추천)한 후 질문 상세 화면을 다시 보여주기 위해 redirect 함수를 사용  # pybo:detail 별칭에 해당하는 페이지로 이동
            # pybo:detail 별칭에 해당하는 URL은 question_id가 필요하므로 question.id를 인수로 전달
            # '{}#answer_{}'.format(resolve_url()) : 답변을 작성한 후 답변글 위치로 다시 이동시키기 위한 앵커 태그 관련 코드
            # resolve_url : 실제 호출되는 URL 문자열을 리턴하는 장고의 함수
            # pybo:detail URL에 #answer_2와 같은 앵커를 추가하기 위해 resolve_url 함수를 사용
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))

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
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
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

# 답변 추천 관련 함수 뷰
@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    # 본인 추천을 방지하기 위해, 로그인한 사용자와 추천하려는 답변의 작성자가 동일할 경우에는 추천할 수 없게 함.
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        # Answer 모델의 voter는 여러 사람을 추가할 수 있는 ManyToManyField이므로, answer.voter.add(request.user) 처럼 add 함수를 사용하여 추천인을 추가한다.
        # 동일한 사용자가 동일한 질문을 여러 번 추천하더라도 추천수가 증가하지는 않는다. ManyToManyField 내부에서 자체적으로 이와 같이 처리한다.
        answer.voter.add(request.user)
    # 질문 상세 페이지로 이동
    return redirect('{}#answer_{}'.format(
        resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
