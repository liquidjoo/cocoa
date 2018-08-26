# -*- coding: utf-8 -*-

import os
from flask import render_template, request, redirect, url_for, session, \
    current_app, jsonify
from werkzeug.security import generate_password_hash
from wtforms import Form, StringField, PasswordField, HiddenField, validators

from photolog.photolog_logger import Log
from photolog.photolog_blueprint import photolog
from photolog.database import dao
from photolog.model.user import User
# from photolog.controller.login import


@photolog.route('/user/regist')
def register_user_form():
    """포토로그 사용자 등록을 위한 폼을 제공하는 함수"""

    form = RegisterForm(request.form)

    return render_template('../photolog/templates/regist.html', form=form)



class RegisterForm(Form):
    """사용자 등록 화면에서 사용자명, 이메일, 비밀번호, 비밀번호 확인값을 검증"""

    username = StringField('Username',
                           [
                               validators.DataRequired('사용자명을 입력하세요'),
                               validators.Length(
                                   min=4,
                                   max=50,
                                   message='4자리 이상 50자리 이하로 입력'
                               )
                           ])

    email = StringField('Email',
                        [
                            validators.DataRequired('이메일을 입력하세요.'),
                            validators.Length(
                                min=4,
                                max=50,
                                message='형식에 맞지 않는 이메일입니다.'
                            )
                        ])

    password = \
        PasswordField('New Password',
                      [
                          validators.DataRequired('비밀번호를 입력하세요'),
                          validators.Length(
                              min=4,
                              max=50,
                              message='4자리 이상 50자리 이하로 입력'
                          ),
                          validators.EqualTo(
                              'password_confirm',
                              message='비밀번호가 일치하지 않습니다.'
                          )
                      ])

    password_confirm = PasswordField('Confirm Password')

    username_check = \
        HiddenField('Username Check',
                    [
                        validators.DataRequired('사용자명 중복을 확인하세요.')
                    ])


class UpdateForm(Form):
    """사용자 등록 화면에서 사용자명, 이메일, 비밀번호, 비밀번호 확인값을 검증함"""

    username = StringField('Username')

    email = StringField('Email',
                        [
                            validators.DataRequired('이메일을 입력하세요.'),
                            validators.Email(message='형식에 맞지 않는 이메일입니다.')
                        ])

    password = \
        PasswordField('New Password',
                      [
                          validators.DataRequired('비밀번호를 입력하세요.'),
                          validators.Length(
                              min=4,
                              max=50,
                              message='4자리 이상 50자리 이하로 입력하세요.'
                          ),
                          validators.EqualTo('password_confirm', message='비밀번호가 일치하지 않습니다.')
                      ])

    password_confirm = PasswordField('Confirm Password')