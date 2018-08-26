"""
    로그인 확인 데코레이터와 로그인 처리 모듈
"""

from flask import render_template, request, current_app, session, redirect \
    , url_for
from functools import wraps
from werkzeug.security import check_password_hash
from wtforms import Form, TextField, PasswordField, HiddenField, validators, StringField

from photolog.database import dao
from photolog.photolog_logger import Log
from photolog.photolog_blueprint import photolog
from photolog.model.user import User



class LoginForm(Form):
    """로그인 화면에서 사용자명과 비밀번호 입력값을 검증"""

    username = \
        StringField('Username',
                    [
                        validators.DataRequired('사용자명을 입력하세요.'),
                        validators.Length(
                            min=4,
                            max=50,
                            message='4자리 이상 50자리 이하로 입력.')
                    ])

    password = PasswordField('New Password',
                             [
                                 validators.DataRequired('비밀번호를 입력하세요'),
                                 validators.Length(
                                     min=4,
                                     max=50,
                                     message='4자리 이상 50자리 이하로 입력하세요.')
                             ])

    next_url = HiddenField('Next URL')