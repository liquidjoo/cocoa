from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # if request.method == 'POST':
    #
    #     # if valid_login(request.form['username'], request.form['password']):
    #     #     return


if __name__ == '__main__':
    app.debug = True
    app.run()
