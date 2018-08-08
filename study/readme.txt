#### 2018. 08. 03

Life is too short, You need Python

파이썬은 Battery Included 개념을 기본으로 하고 있다.


Full stack Framework vs Micro Framework

대표적인예로

Full stack 은 Django, Micro Flask


앞으로 사용할 파이썬 기반의 프레임워크는 Flask!!

Flask 특징

기본적으로 WSGI(Web Server Gateway Interface) 구현체인 벡자이크(WerkZeug)와 템플릿 엔진인 신사2(Jinja2)로 구성
WSGI는 일종의 애플리케이션 컨테이너 역할을 정의한 파이썬 표준.
간단한 코어엔진을 제공하지만 쉽게 확장하여 사용할 수 있게 여러 가지 확장 기능을 지원한다.
 - 개발용 서버와 디버거 내장
 - 단위테스트와 통합 지원
 - RESTful 요청 처리
 - 템플릿 엔진 내장
 - 안전한 쿠키 지원 (secure cookie)
 - WSGI 1.0 호환
 - 구글 앱 엔진 호환 등.

Flask 기본 원리

url call -> route decorator(view function call) -> template -> user

route decorator
url에 맵핑된 함수를 찾아 실행
(참고: 위키북스 '프로가 되기 위한 웹 입문 기술'

인코딩 선언
# -*- coding: utf-8 -*-


### 2018. 08. 08

local 에서 특정 요청에 대한 메소드 테스트
app.test_request_context() 를 이용해 url_for() 함수로 반환되는 URI를 찾을 수 있다.
* 화면 템플릿에 URI를 하드코딩하지 않고 url_for() 함수를 사용해 URI를 동적으로 생성하면 아래와 같은 장점을 갖는다
URI를 변경해야 할 경우, route() 데코레이터에 지정된 URI만 수정하면 된다.
url_for() 함수로 생성되는 URI는 특수문자와 유니코드 변환을 자동으로 해준다.
URI의 접두어가 루트('/')가 아니더라도 url_for() 함수가 설정된 애플리케이션 루트에 URI의 접두어를 붙여서 처리


요청과 응답
요청
플라스크에서 요청에 대한 정보는 전역 객체인 request에 담겨있고, 이 객체는 스레드에 대해 안전(thread-safe)을 보장 한다.
(* thread-safe: 하나의 함수가 한 스레드로부터 호출되어 실행 중일 때, 다른 스레드가 그 함수를 호출하여 동시에 함께 실행되더라도 각 스레드에서의 함수의 수행 결과가 올바로 나오는 것으로 정의)

ex) username 같은 항목이 GET 방식의 인자로 넘어왔다면 request.args.get['username'] 으로 값을 얻을 수 있다.
form, args 모두 플라스크의 기반 툴킷인 벡자이크(werkzeug)에서 제공하는 MultiDict 타입이므로 같은 키로 여러 개의 값을 가질 수 있다.

응답
요청에 대한 로직이 끝났으면 반환을 해야하는데 플라스크에서는 자동으로 response 객체로 변환한다.
뷰 함수의 리턴값을 문자열로 넘겨주면 플라스크는 자동으로 text/html 형태의 문자열을 가진 HTTP 응답으로 변환하지만
뷰 함수의 리턴값은 기본적으로 (response, status=None, headers=None) 튜플로 넘겨진다.
만약 response 객체 생성 후 헤더 정보를 추가하거나 response 객체를 수정해야 하는 일이 생긴다면 make_response() 함수를 사용해 추가할 수 있다.

ex)
def index():
    response = make_response(render_template('index.html', foo=42))
    response.headers['X-Parachutes'] = 'paracutes are cool'
    return response

