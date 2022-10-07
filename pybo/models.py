# 장고 모델
# 장고에서 모델은 데이터베이스의 구조(layout)를 의미한다.
# models.py 파일에 하나 이상의 모델 클래스를 정의해 데이터베이스의 테이블을 정의할 수 있다.


from django.db import models
from django.contrib.auth.models import User


# 질문 모델
class Question(models.Model):
    # 작성자 컬럼
    # User 모델 : django.contrib.auth 앱이 제공하는 사용자 모델. 우리는 회원 가입 시 데이터 저장에 사용했던 모델이다.
    # models.ForeignKey : 타 모델(User)을 속성으로 연결
    # on_delete=models.CASCADE : 계정(User)이 삭제되면 이 계정이 작성한 질문을 모두 삭제
    # related_name='author_question' : 특정 사용자가 작성한 질문을 가져오기 위한 코드. [특정 사용자].author_question.all() 처럼 사용해 특정 사용자가 작성한 모든 질문을 가져올 수 있다.
    # Question 모델에서 사용한 author와 voter가 모두 User 모델과 연결되어 있기 때문에, User.question_set 처럼 User 모델을 통해서 Question 데이터에 접근하려고 할 때,
    # author를 기준으로 할지 voter를 기준으로 해야 할지 명확하지 않다는 오류가 발생하기에 related_name='author_question'와 같이 그 대상을 명확히 지정해 줌.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    # 제목
    # 최대 200자
    # CharField : 글자수의 길이가 제한된 텍스트에 사용
    subject = models.CharField(max_length=200)
    # 내용
    # TextField : 글자수를 제한할 수 없는 텍스트에 사용
    content = models.TextField()
    # 작성 일시
    create_date = models.DateTimeField()
    # 수정 일시 컬럼
    # null=True : 데이터베이스에서 해당 컬럼에 null을 허용한다는 의미
    # blank=True : form.is_valid()를 통한 입력 데이터 검증 시 값이 없어도 된다는 의미
    # 수정 일시는 수정한 경우에만 생성되는 데이터이므로, 어떤 조건으로든 값을 비워둘 수 있음을 의미하는 null=True, blank=True를 지정
    modify_date = models.DateTimeField(null=True, blank=True)
    # 추천인 컬럼
    # User 모델을 ManyToManyField 관계로 연결. 다대다(N:N) 관계
    # related_name='voter_question' : 특정 사용자가 추천한 질문 데이터를 얻기 위해서는 [특정 사용자].voter_question.all() 처럼 사용해 가져올 수 있다.
    voter = models.ManyToManyField(User, related_name='voter_question')

    # __str__ 메서드(string 메서드)
    # : 장고 모델에서 클래스의 오브젝트를 출력할 때 나타날 내용들을 결정하는 메서드
    def __str__(self):
        # 모델 데이터 조회 시, Question 모델에 저장된 값들의 제목이 표시되도록 설정함
        return self.subject  # 제목 표시

# 답변 모델
class Answer(models.Model):
    # 작성자 컬럼
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    # 질문 모델을 속성으로 연결. (해당 답변과 관련된) 질문
    # models.ForeignKey : 타 모델(Question)을 외래키로 연결
    # on_delete=models.CASCADE : 해당 답변과 연결된 질문이 삭제될 경우 답변도 함께 삭제됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 내용
    content = models.TextField()
    # 작성 일시
    create_date = models.DateTimeField()
    # 수정 일시 컬럼
    modify_date = models.DateTimeField(null=True, blank=True)
    # 추천인 컬럼
    voter = models.ManyToManyField(User, related_name='voter_answer')