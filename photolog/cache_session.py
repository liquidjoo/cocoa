# -*- coding: utf-8 -*-


from datetime import timedelta
from uuid import uuid4
from werkzeug.contrib.cache import NullCache, SimpleCache, RedisCache
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin


# CacheSession Class는 open_session() 메서드에서 결과값으로 반환하는 클래스로 딕셔너리의 변화를 감시하여
# 정해진 콜백 함수를 호출하는 CallbackDict 클래스와 세션의 몇 가지 속성을 사용하기 위해 SessionMixin 클래스를 상속
class CacheSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):

        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


# 서버 측 세션 구현에 가장 중요한 CacheSessionInterface
# open_session, save_session 메서드를 캐시를 이용해 오버라이드
class CacheSessionInterface(SessionInterface):
    session_class = CacheSession

    def __init__(self, cache=None, prefix='cache_session'):
        if cache is None:
            cache = NullCache()
        self.cache = cache
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_cache_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)

        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)

        val = self.cache.get(self.prefix + sid)
        if val is not None:
            return self.session_class(val, sid=sid)
        return self.session_class(sid=sid, new=True)

    # save_session 메서드는 요청이 완료되는 시점에 호출
    # 세션에 값이 없으면(딕셔너리 형태의 세션에 어떤 값도 없으면), 캐시에서 그 세션에 대해 저장된 값을 삭제
    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)

        if not session:
            self.cache.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)

            return

        cache_exp = self.get_cache_expiration_time(app, session)

        val = dict(session)
        self.cache.set(self.prefix + session.sid, val, int(cache_exp.total_seconds()))

        response.set_cookie(app.session_cookie_name,
                            session.sid,
                            httponly=True,
                            domain=domain)


# 세션을 유지하는데 사용한 캐시의 종류에 따른 클래스 구현

# __init__() 함수의 인자인 cache에 세션을 유지할 캐시 종류를 설정
class SimpleCacheSessionInterface(CacheSessionInterface):

    def __init__(self):

        CacheSessionInterface.__init__(self,
                                       cache=SimpleCache(),
                                       prefix='simple_cache_session:')


class RedisCacheSessionInterface(CacheSessionInterface):

    def __init__(self,
                 host='localhost',
                 port=6379):
        cache = RedisCache(host=host, port=port)
        CacheSessionInterface.__init__(self,
                                       cache,
                                       prefix='redis_cache_session:')