# 장고 폼
# 폼은 쉽게 말해 페이지 요청 시 전달되는 파라미터들을 쉽게 관리하기 위해 사용하는 클래스이다.
# 폼은 필수 파라미터의 값이 누락되지 않았는지, 파라미터의 형식은 적절한지 등을 검증할 목적으로 사용한다.
# 이 외에도 HTML을 자동으로 생성하거나 폼에 연결된 모델을 이용하여 데이터를 저장하는 기능도 있다.


from django import forms
from pybo.models import Question


# Question 모델과 연결된 폼
# 모델 폼(forms.ModelForm) : 모델(Model)과 연결된 폼으로, 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있는 폼
# 장고의 폼은 일반 폼(forms.Form)과 모델 폼(forms.ModelForm)이 있다.
class QuestionForm(forms.ModelForm):
    class Meta:  # 모델 폼은 이너 클래스인 Meta 클래스가 반드시 필요  # Meta 클래스에는 사용할 모델과 모델의 속성을 적어야 한다.
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        # 위젯 속성
        # widgets 속성을 지정하면 subject, content 입력 필드에 form-control과 같은 부트스트랩 클래스를 추가해 (질문 등록 페이지에) 디자인을 적용할 수 있다.
        # question_form.html의 {{ form.as_p }} 태그로 인해, 부트스트랩을 적용할 수가 없어서 위와 같이 위젯 속성을 활용
        # {{ form.as_p }} 태그는 HTML 코드를 자동으로 생성하기 때문에.
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        # labels 속성
        # 질문 등록 페이지에 표시되는 'Subject', 'Content'를 한글로 표시하기
        labels = {
            'subject': '제목',
            'content': '내용',
        }