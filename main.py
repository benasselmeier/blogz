from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists

# THINGS TO ASK ABOUT:
# Sign Up function: will show "duplicate user" error, but after showing "invalid username" error, won't go back to showing "duplicate user"
# under the correct conditions.
#
#
#
#
#
#


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, entry, author):
        self.name = name
        self.entry = entry
        self.author = author


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='author')
       
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['POST', 'GET'])
def home_redirect():

    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def display_blog():

    blog_id = request.args.get('id')
    if blog_id == None:
        blog_entries = Blog.query.all()
    else:
        blog_entry = Blog.query.get(int(blog_id))
        if blog_entry == None:
            print(blog_entry)
            return redirect('/blog')
        blog_entries = [blog_entry]
    return render_template('blog.html', title="Build-a-Blog!", blog_entries=blog_entries)
    
# TODO: Sign Up Function:
# User enters a valid new username and password, and is redirected to the /newpost page with their username stored in a session.
# User gets an error message if:
#   username, password, or verify forms are blank, invalid, or passwords don't match
#   username already exists in the database

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error = " "
        password_error = " "
        verify_error = " "

        if len(username) >= 3 and " " not in username:
            username = username
        else:
            username = " "
            username_error = "Invalid username!"

        if len(password) >= 3 and " " not in password and password == verify:
            password = password
        else:
            password = " "
            password_error = "Invalid password!"

        if verify == password:
            verify = verify
        elif verify != password and password == " ":
            verify = " "
        else:
            verify_error = "Passwords don't match!"

        rules = (username_error == " ", password_error == " ", verify_error == " ")

        if all(rules):
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                print("it's a new user!")
                return redirect('/newpost')
            else:
                print("Duplicate user")
                duplicate_error = "Duplicate user!"
                return render_template('signup.html', duplicate_error=duplicate_error)
        else:
            return render_template('signup.html', username=username, username_error=username_error, password_error=password_error, verify_error=verify_error)

    return render_template('signup.html')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['entry']
        author = Blog.owner_id

        if title == "" or entry == "":
            flash("Title and entry must contain text!", "error")
            title = title
            entry = entry
            return render_template('newpost.html', title=title, entry=entry)
        else:
            blog_entry = Blog(title, entry, author)
            db.session.add(blog_entry)
            db.session.commit()
            return redirect('/blog?id=' + str(blog_entry.id))

    return render_template('newpost.html')


if __name__ == '__main__':
    app.secret_key = "screeblegloobleshmuh"
    app.run()