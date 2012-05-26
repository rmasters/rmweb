from flask import Flask, render_template, abort, make_response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

from models import *

@app.route('/')
def home():
    projects = Project.query.filter(Project.frontpage == True).all()
    links = Link.query.filter(Link.visible == True).all()
    blogs = BlogPost.query.filter(BlogPost.published != None).order_by(BlogPost.published.desc()).limit(5).all()
    return render_template('home.html', projects=projects, links=links, blogs=blogs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    active = []
    inactive = []
    for p in Project.query.all():
        active.append(p) if p.active else inactive.append(p)

    return render_template('projects.html', active=active, inactive=inactive)

@app.route('/projects/<slug>')
def project(slug):
    project = Project.query.filter(Project.slug == slug).one()
    return render_template('project.html', project=project)

@app.route('/blog')
def blog():
    posts = BlogPost.query.filter(BlogPost.published != None).order_by(BlogPost.published.desc()).limit(30).all()
    return render_template('blog.html', posts=posts, labels=BlogLabel.query.all())

@app.route('/blog.rss')
def blog_rss():
    posts = BlogPost.query.filter(BlogPost.published != None).order_by(BlogPost.published.desc()).limit(10).all()

    r = make_response(render_template('blog_feed.xml', posts=posts))
    r.mimetype = 'application/xml'
    return r

@app.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter(BlogPost.slug == slug).one()
    if post is None or post.published is None:
        abort(404)
    return render_template('blog_post.html', post=post, labels=BlogLabel.query.all())

@app.route('/blog/label/<slug>')
def blog_post_label(slug):
    label = BlogLabel.query.filter(BlogLabel.slug == slug).one()
    if label is None:
        abort(404)
    return render_template('blog_label.html', label=label, labels=BlogLabel.query.all())

if __name__ == '__main__':
    app.debug = True
    app.run(host='new.rossmasters.com')
