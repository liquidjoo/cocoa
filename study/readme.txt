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

