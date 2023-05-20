from flask import session, Flask, redirect, url_for, request, render_template, flash, g
import hashlib
import sqlite3

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'0216e3fecbced0c5bd14b5c40a027d81225148d8e3ee994cf2db1bd9ffdf0890'


# accounts = {
    # "kostas": "1234",
    # "efthimis": "5678",
    # "mixalhs": "9101112"
# }
# 
# for user, passw in accounts.items():
    # accounts[user] = hashlib.sha256(passw.encode('utf-8')).hexdigest()
# 
# print(*accounts.items(), sep='\n')

DATABASE = 'database.db'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



def private_page(func, *args, **kwargs):
    def ret(*_args, **_kwargs):
        if 'username' not in session:
            return "You must login first"
        return func(*_args, **_kwargs)
    return ret

with app.app_context():
    for user in query_db('select * from users'):
        print(user['username'], 'has the id', user['user_id'])


@app.route('/profile')
@private_page
def profile():
    profile_data = query_db('select * from profile where user_id = ?',
                            [session['user_id']], one=True)

    print(profile_data)
    return render_template("profile.html", profile_data=profile_data)


@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = query_db('select * from users where username = ?',
                [request.form['username']], one=True)
       
        if user is not None and \
            hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest() == user['password_hash']:
            session['username'] = request.form['username']
            session['user_id'] = user['user_id']
            return redirect('/profile')
        else:
            flash('Kako username h password')
            return redirect(url_for('login'))
        

    
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
