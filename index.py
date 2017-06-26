from flask import Flask,render_template,request,make_response,url_for,redirect
from flask import session
from flask import  _app_ctx_stack,g
import os
import sqlite3

# Flask object
app = Flask(__name__)

# config
DATABASE='test2.db'
DEBUG = True
SECRET_KEY = os.urandom(24)
# load configuration
app.config.from_object(__name__)
app.config.from_envvar("FLASK_SETTING",silent=True)

# init - db
def get_db():
    # create application context
    top = _app_ctx_stack.top
    # if sqlite3 connection not exists,create one
    if not hasattr(top, 'sqlite3'):
        top.sqlite3 = sqlite3.connect(os.path.join(app.root_path, app.config['DATABASE']))
        top.sqlite3.row_factory = sqlite3.Row
    return top.sqlite3;

# route
@app.route('/')
def show_entries():
    records = g.db.execute('select * from entries where 1').fetchall();
    return render_template('show_entries.html',entries=records)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    g.db.execute('insert into entries (title,text) values (?,?)',[request.form['title'],request.form['text']])
    g.db.commit()
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
    if 'islogin' in session:
        return redirect(url_for('show_entries'))
    if request.method == "POST":
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            # login success, write session
            session['username'] = request.form['username']
            session['islogin'] = True
            return redirect(url_for('show_entries'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # clear session
    session.pop('username',None)
    session.pop('islogin', None)
    return redirect(url_for('show_entries'))

@app.route('/signin',methods=['GET','POST'])
def signin():
    return 'Signin'

@app.teardown_appcontext
def close_conn(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite3'):
        top.sqlite3.close()

@app.before_request
def before_requre():
    # get db
    g.db = get_db()


# entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0')