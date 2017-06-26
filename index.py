from flask import Flask,render_template,request,make_response,url_for,redirect
import os

# Flask object
app = Flask(__name__)

# config
DATABASE='test2.db'
DEBUG = True
SECRET_KEY = os.urandom(24)
# load configuration
app.config.from_object(__name__)
app.config.from_envvar("FLASK_SETTING",silent=True)

# route
@app.route('/')
def show_entries():
    return render_template('show_entries.html')

@app.route('/addentry', methods=['POST'])
def add_entry():
    pass

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        pass
    return render_template('login.html')

@app.route('/logout')
def logout():
    # clear session
    return redirect(url_for('show_entries'))

# entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0')