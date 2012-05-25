from web import db
import markdown
import re

def create_slug(input):
    return re.sub('[^a-z0-9-_]', '-', input.lower())

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    label = db.Column(db.Text)
    # Whether the link is visible
    visible = db.Column(db.Boolean)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    slug = db.Column(db.Text)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    # Whether the project is shown on the frontpage
    frontpage = db.Column(db.Boolean)
    # Is the project being worked on at the moment?
    active = db.Column(db.Boolean)
    assoc_label = db.Column('label', db.Integer, db.ForeignKey('blog_label.id'))

    def content_as_html(self):
        return markdown.markdown(self.content)

    def __repr__(self):
        print self.name

blog_post_labels = db.Table('post_label',
    db.Column('post', db.Integer, db.ForeignKey('blog_post.id')),
    db.Column('label', db.Integer, db.ForeignKey('blog_label.id')))

class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    slug = db.Column(db.Text)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime, nullable=True)
    published = db.Column(db.DateTime, nullable=True)

    labels = db.relationship('BlogLabel', secondary=blog_post_labels, backref='posts')

    def content_as_html(self):
        return markdown.markdown(self.content)

class BlogLabel(db.Model):
    __tablename__ = 'blog_label'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    slug = db.Column(db.Text)
    description = db.Column(db.Text)

    project = db.relationship('Project', backref='label', uselist=False)

    def published_posts(self):
        posts = [post for post in self.posts if post.published != None]
        return posts

    def description_as_html(self):
        return markdown.markdown(self.description)
