from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists

# stopped at newpost step for the night


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