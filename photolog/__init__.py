# -*- coding: utf-8 -*-


import os
from flask import Flask, render_template, request, url_for


def print_settings(config):
    print('=======================================================')
    print('SETTINGS for PHOTOLOG APPLICATION')
    print('=======================================================')
    for key, value in config:
        print('%s=%s' % (key, value))
    print('=======================================================')

    ''' HTTP Error Code 404와 500은 errorhandler에 application 레벨에서
        적용되므로 app 객체 생성시 등록해준다. 
    '''


def not_found(error):
    return render_template('404.html'), 404


def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def create_app(config_filepath='resource/config.cfg'):
    photolog_app = Flask(__name__)

    # 기본 설정은 PhotologConfig 객체에 정의되있고 운영 환경 또는 기본 설정을 변경을 하려면
    # 실행 환경변수인 PHOTOLOG_SETTINGS에 변경할 설정을 담고 있는 파일 경로를 설정
    