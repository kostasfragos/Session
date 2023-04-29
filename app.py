from flask import session, Flask, redirect, url_for, request, render_template, flash

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'0216e3fecbced0c5bd14b5c40a027d81225148d8e3ee994cf2db1bd9ffdf0890'


accounts = {
    "kostas": "1234",
    "nikos": "5678",
    "giannhs": "9101112"
}

def private_page(func, *args, **kwargs):
    def ret(*_args, **_kwargs):
        if 'username' not in session:
            return "You must login first"
        return func(*_args, **_kwargs)
    return ret


@app.route('/secret')
@private_page
def secret():
    return "ONLY LOGGED IN USERS SHOULD SEE THIS"

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] in accounts and request.form['password'] == accounts[request.form['username']]:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            flash('Kako username h password')
            return redirect(url_for('login'))
        

    
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
