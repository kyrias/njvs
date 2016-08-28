from flask import Flask
from flask import render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///njvs.db'
db = SQLAlchemy(app)

class languages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), unique=True)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creationDate = db.Column(db.Date)
    username = db.Column(db.String(255), unique=True)
    displayname = db.Column(db.String(255))

    words = db.relationship('words', backref='creator')
    definitions = db.relationship('definitions', backref='creator')


class types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), unique=True)

    words = db.relationship('words', backref='type')


class words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeId = db.Column(db.Integer, db.ForeignKey('types.id'))
    creatorId = db.Column(db.Integer, db.ForeignKey('users.id'))
    creationDate = db.Column(db.Date)
    word = db.Column(db.String(255), unique=True)

    definitions = db.relationship('definitions', backref='word')


definition_tags_association = db.Table('definition_tags',
    db.Column('definitionId', db.Integer, db.ForeignKey('definitions.id')),
    db.Column('tagId', db.Integer, db.ForeignKey('tags.id'))
)

class definitions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wordId = db.Column(db.Integer, db.ForeignKey('words.id'))
    languageId = db.Column(db.Integer, db.ForeignKey('languages.id'))
    creatorId = db.Column(db.Integer, db.ForeignKey('users.id'))
    creationDate = db.Column(db.Date)
    definition = db.Column(db.Text)
    notes = db.Column(db.Text)
    etymology = db.Column(db.Text)

    tags = db.relationship('tags', secondary=definition_tags_association)
    language = db.relationship('languages')


class tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255), unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))


@app.route('/users/')
def show_users():
    us = users.query.all()
    return render_template('users.html', users=us)


@app.route('/words/<word>')
def show_word(word):
    word = words.query.filter_by(word=word).first()
    return render_template('word.html', word=word)