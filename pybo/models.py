# 장고 모델
# 장고에서 모델은 데이터베이스의 구조(layout)를 의미한다.
# models.py 파일에 하나 이상의 모델 클래스를 정의해 데이터베이스의 테이블을 정의할 수 있다.


from django.db import models


# 질문 모델
class Question(models.Model):
    # 제목
    # 최대 200자
    # CharField : 글자수의 길이가 제한된 텍스트에 사용
    subject = models.CharField(max_length=200)
    # 내용
    # TextField : 글자수를 제한할 수 없는 텍스트에 사용
    content = models.TextField()
    # 작성 일시
    create_date = models.DateTimeField()

    # __str__ 메서드
    # 장고 모델에서 클래스의 오브젝트를 출력할 때 나타날 내용들을 결정하는 메서드
    def __str__(self):
        # 모델 데이터 조회 시, Question 모델에 저장된 값들의 제목이 표시되도록 설정함
        return self.subject  # 제목 표시

# 답변 모델
class Answer(models.Model):
    # (해당 답변과 관련된) 질문
    # models.ForeignKey : 기존 타 모델(question)을 속성으로 연결
    # on_delete=models.CASCADE : 해당 답변과 연결된 질문이 삭제될 경우 답변도 함께 삭제됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 내용
    content = models.TextField()
    # 작성 일시
    create_date = models.DateTimeField()