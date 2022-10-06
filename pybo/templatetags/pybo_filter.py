# 템플릿 필터 직접 작성

# 빼기 기능 관련 템플릿 필터 직접 작성  #  |sub:[숫자] 와 같은 기능

from django import template


register = template.Library()


# 빼기 기능 관련 템플릿 필터 직접 작성  #  |sub:[숫자] 와 같은 기능
# 빼기 기능 관련 필터
# sub 함수 : 기존 값 value에서 입력으로 받은 값 arg를 빼서 리턴하는 함수
# @register.filter 애너테이션 : 템플릿에서 해당 함수를 필터로 사용할 수 있게 함
@register.filter
def sub(value, arg):
    return value - arg