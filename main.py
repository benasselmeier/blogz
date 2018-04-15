from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(1000))

    def __init__(self, name, entry):
        self.name = name
        self.entry = entry


@app.route('/', methods=['POST', 'GET'])
def index():

    blog_entries = Blog.query.all()

    return render_template('blog.html',title="Build-a-Blog!", blog_entries=blog_entries)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    blog_entries = Blog.query.all()

    if request.method == 'POST':
        title_input = request.form['blog-title']
        content_input = request.form['blog-entry']

        if title_input == "" or content_input == "":
            flash("Title and entry must contain text!")
        else:
            blog_entry = Blog(title_input, content_input)
            db.session.add(blog_entry)
            db.session.commit()
            return redirect('/')


    return render_template('newpost.html',title="Build-a-Blog!", blog_entries=blog_entries)

if __name__ == '__main__':
    app.run()