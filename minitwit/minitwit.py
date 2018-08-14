# -*- coding: utf-8 -*-

from __future__ import with_statement
import time
from sqlite3 import dbapi2 as sqllite3
from hashlib import md5
from datetime import datetime
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash
from werkzeug.security import check_password_hash, generate_password_hash

# configuration
DATABASE = 'twit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
# __name__ 모듈의 이름 == __main__ 이 되면 주 프로그렘
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)


# 공통으로 사용할 데이터베이스 관련 함수 정의
def connect_db():
    """Returns a new connection to the database."""
    return sqllite3.connect(app.config['DATABASE'])


# 데이터베이스 질의하는 부분은 기능별 함수에 따라 다르지만, 데이터베이스 연결과 종료는 모든 기능에서 동일하게 수행
# 플라스크에서는 before_request()와 teardown_request() 데코레이터를 이용해 좀 더 모듈화 할 수 있다.

# before_first_request : 웹 application 기동 이후 가장 처음에 들어오는 HTTP 요청에서만 실행
#
# before_request : HTTP 요청이 들어올때마다 실행
#
# after_request : HTTP 요청이 끝나고 브라우저에 응답하기 전에 실행
#
# teardown_request : HTTP 요청 결과가 브라우저에 응답한 다음 실행
#
# teardown_appcontext : HTTP 요청이 완전히 완료되면 실행
# before_first_request, before_request는 어떠한 인자도 전달할수 없다
#
# after_request는 flask.wrapper.Response 객체를 return 해야한다
@app.before_request
def before_request():
    """Make sure we are connected to the database each request an look up the current user so that we know he's there"""
    g.db = connect_db()
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


# g 전역(global) 객체를 의미, 다만 한 번의 요청에 대해서만 같은 값을 유지하고 스레드에 대해 안전하다는 전제조건이 있
@app.teardown_request
def teardown_request():
    """Closes the database agagin at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


# 데이터베이스 질의를 쉽게 처리할 수 있는 공통 함수 작성
def query_db(query, args=(), one=False):
    """Queries the database an returns a list of dictionaries."""
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    """Convenience method to look up the id for a username"""
    rv = g.db.execute('select user_id from user where username = ?',
                      [username]).fetchone()
    return rv[0] if rv else None

def init_db():
    """Creates the database tables"""
    with closing(connect_db()) as db:
        with app.open_resource('shema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# 뷰 함수 구현 - 사용자 등록
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None

    if request.method =='POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
            '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            g.db.execute('''insert into user (
                username, email, pw_hash) values (?, ?, ?)''',
                [request.form['username'], request.form['email'],
                 generate_password_hash(request.form['password'])
                 ])
            g.db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
        return render_template('twit/register.html', error=error)


# 로그인 로그아웃
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'], request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('timeline'))
    return render_template('twit/login.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    # session.pop 세션 삭제
    session.pop('user_id', None)
    return redirect(url_for('public_timeline'))


@app.route('/add_message', methods=['POST'])
def add_message():
    """Registers a new message for the user"""
    if 'user_id' not in session:
        abort(401)
    if request.form['text']:
        g.db.execute('''insert into
            message (author_id, text, pub_date)
            values (?, ?, ?)''', (session['user_id'],
                                  request.form['text'],
                                  int(time.time())))
        g.db.commit()
        flash('Your message was recorded')
    return redirect(url_for('timeline'))


def gravatar_url(email, size=80):
    """Return the gravatar image for the given eamil address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
           (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.route('/<username>/follow')
def follow_user(username):
    """Adds the current user as follower of the given user."""
    if not g.user:
        abort(401)
    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    g.db.execute('insert into follower (who_id, whom_id) values (?, ?)',
                 [session['user_id'], whom_id])
    g.db.commit()
    flash('You are now following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))




if __name__ == '__main__':

    init_db()
    app.run()
