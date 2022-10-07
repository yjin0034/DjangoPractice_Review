# 템플릿 필터 직접 작성


import markdown
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


# 빼기 기능 관련 템플릿 필터 직접 작성  #  |sub:[숫자] 와 같은 기능
# 빼기 기능 관련 필터
# sub 함수 : 기존 값 value에서 입력으로 받은 값 arg를 빼서 리턴하는 함수
# @register.filter 애너테이션 : 템플릿에서 해당 함수를 필터로 사용할 수 있게 함
@register.filter
def sub(value, arg):
    return value - arg


# 마크다운 관련 필터
# mark 함수 : markdown 모듈과 mark_safe 함수를 이용하여 입력 문자열을 HTML로 변환하는 필터 함수
@register.filter
def mark(value):
    # nl2br, fenced_code : 마크다운 확장 기능
    # nl2br : 줄바꿈 문자를 <br> 로 바꾸어 주는 기능. nl2br을 사용하지 않을 경우, 줄바꿈을 하기 위해서는 줄 끝에 스페이스(' ')를 두개 연속으로 입력해야 함.
    # fended_code : 마크다운의 소스코드 표현을 위해 필요
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))