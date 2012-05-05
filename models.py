from web import db
import markdown

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

    def content_as_html(self):
        return markdown.markdown(self.content)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    slug = db.Column(db.Text)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime, nullable=True)
    published = db.Column(db.DateTime, nullable=True)

    def content_as_html(self):
        return markdown.markdown(self.content)
