from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists


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

        if title == "" or entry == "":
            flash("Title and entry must contain text!", "error")
            title = title
            entry = entry
            return render_template('newpost.html', title=title, entry=entry)
        else:
            blog_entry = Blog(title, entry)
            db.session.add(blog_entry)
            db.session.commit()
            return redirect('/blog?id=' + str(blog_entry.id))

    return render_template('newpost.html')


if __name__ == '__main__':
    app.secret_key = "screeblegloobleshmuh"
    app.run()