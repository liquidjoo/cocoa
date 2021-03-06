import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response
from contextlib import closing

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# Flask 객체를 생성, 플라스크 애플리케이션 모듈명을 Flask 클래스의 첫 번째 인자로 넘겨주며 플라스크 어플리케이션 객체인 app을 생성
# 이 객체로 모든 플라스크 기능을 사용
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    app.run()

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] !=app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# def index():
#     response = make_response(render_template('index.html', foo=42))
#     response.headers['X-Parachutes'] = 'paracutes are cool'
#     return response

# #쿠키 정보 접근
# @app.route('/')
# def index():
#     username = request.cookies.get('username')
#
# #쿠키 값 설정
# @app.route('/')
# def index():
#     resp = make_response(render_template('index.html'))
#     resp.set_cookie('username', 'flask')
#     return resp

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404


# app.logger.debug('error message')
# app.logger.warning('error message')
# app.logger.error('error message')
