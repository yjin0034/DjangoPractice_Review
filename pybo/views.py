# 장고 뷰
# 장고에서 뷰는 어떤 데이터를 표시할지 정의하며, HTTP 응답 상태 코드(response)를 반환한다.
# views.py 파일에 애플리케이션의 처리 논리를 정의한다.
# 사용자가 입력한 URL에 따라, 모델(Model)에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, 템플릿(Template)에 전달하는 역할을 한다.
# 장고의 뷰 파일(views.py)은 요청에 따른 처리 논리를 정의한다.
# 즉, 사용자가 요청하는 값(request)을 받아 모델과 템플릿을 중개하는 역할을 한다.


from django.http import HttpResponse


# index 페이지 관련 함수
# index 함수의 매개변수 request는 HTTP 요청 객체
def index(request):
    # HttpResponse : 요청에 대한 응답을 할 때 사용
    return HttpResponse("안녕하세요 pybo에 오신 것을 환영합니다.")

