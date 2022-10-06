from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# 회원가입 계정 생성 시 사용할 폼
# UserForm은 django.contrib.auth.forms 모듈의 UserCreationForm 클래스를 상속하여 만듦
# UserForm을 따로 만들지 않고 UserCreationForm을 그대로 사용해도 되지만, 이메일 등의 추가적인 속성을 추가하기 위해서는 UserCreationForm 클래스를 상속하여 새 클래스를 만들어야 한다.
class UserForm(UserCreationForm):
    # 이메일 속성(필드) 추가
    email = forms.EmailField(label="이메일")
    class Meta:  # 이너 클래스인 Meta 클래스가 반드시 필요  # Meta 클래스에는 사용할 모델과 모델의 속성을 적어야 한다.
        model = User  # 사용할 모델  # User 모델과 연결
        fields = ("username", "password1", "password2", "email")  # UserForm에서 사용할 User 모델의 속성(필드)
        # username	사용자이름
        # password1	비밀번호1
        # password2	비밀번호2 (비밀번호1을 제대로 입력했는지 대조하기 위한 값)
        # UserCreationForm의 is_valid 함수는 폼에 위의 속성 3개가 모두 입력되었는지, 비밀번호1과 비밀번호2가 같은지, 비밀번호의 값이 비밀번호 생성 규칙에 맞는지 등을 검사하는 로직을 내부적으로 가지고 있음
