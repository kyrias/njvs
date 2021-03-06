from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///njvs.db',
    SECRET_KEY='xkFFngMCcZrMVmGt1MZ7ir9+3TCKJISBfiSHup1wYclQSRDjag+YvctvWxW2Ghi'
))
db = SQLAlchemy(app)


class languages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(3), unique=True)
    name = db.Column(db.String(25), unique=True)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creationDate = db.Column(db.Date)
    username = db.Column(db.String(20), unique=True)
    displayname = db.Column(db.String(20))

    words = db.relationship('words', backref='creator')
    definitions = db.relationship('definitions', backref='creator')


class types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True)

    words = db.relationship('words', backref='type')


class words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeId = db.Column(db.Integer, db.ForeignKey('types.id'))
    creatorId = db.Column(db.Integer, db.ForeignKey('users.id'))
    creationDate = db.Column(db.Date)
    word = db.Column(db.String(50), unique=True)

    definitions = db.relationship('definitions', backref='word')


definition_glosswords_association = db.Table('definition_glosswords',
    db.Column('definitionId', db.Integer, db.ForeignKey('definitions.id')),
    db.Column('glosswordId', db.Integer, db.ForeignKey('glosswords.id'))
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

    glosswords = db.relationship('glosswords', secondary=definition_glosswords_association)
    language = db.relationship('languages')


class glosswords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    glossword = db.Column(db.String(50), unique=True)
    definitions = db.relationship('definitions', secondary=definition_glosswords_association)


@app.route('/users/')
def show_users():
    us = users.query.all()
    return render_template('users.html', users=us)


@app.route('/words/')
def show_words():
    ws = words.query.all()

    return render_template('words.html', words=ws)


@app.route('/words/<word>')
def show_word(word):
    word = words.query.filter_by(word=word).first()
    defs = {}

    for definition in definitions.query.filter_by(wordId=word.id).all():
        lang = definition.language.name
        if lang not in defs:
            defs[lang] = []

        defs[lang].extend([definition])

    return render_template('word.html', word=word, definitions=defs)


@app.route('/glosswords/<glossword>')
def show_glossword(glossword):
    glossword = glosswords.query.filter_by(glossword=glossword).first()

    defs = {}
    for definition in glossword.definitions:
        defs[definition.wordId] = definition

    return render_template('glossword.html', glossword=glossword, definitions=defs)
