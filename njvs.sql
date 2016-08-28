CREATE TABLE languages (
	id INTEGER PRIMARY KEY,
	tag VARCHAR(3) UNIQUE, -- ISO 639-3 code
	name VARCHAR(25) UNIQUE
);
INSERT INTO languages (tag, name)
       VALUES ("jbo", "la lojban");
INSERT INTO languages (tag, name)
       VALUES ("eng", "English");



CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	creationDate DATETIME,
	username VARCHAR(20) UNIQUE,
	displayname VARCHAR(20)
);
INSERT INTO users (username, displayname)
       VALUES ("kyrias", "Johannes Löthberg");



CREATE TABLE types (
	id INTEGER PRIMARY KEY,
	type VARCHAR(20) UNIQUE
);
INSERT INTO types (type) VALUES ('gismu');
INSERT INTO types (type) VALUES ('lujvo');
INSERT INTO types (type) VALUES ('cmavo');
INSERT INTO types (type) VALUES ('cmavo-compound');
INSERT INTO types (type) VALUES ('cmevla');
INSERT INTO types (type) VALUES ("fu'ivla");
INSERT INTO types (type) VALUES ('experimental gismu');
INSERT INTO types (type) VALUES ('experimental cmavo');



CREATE TABLE words (
	id INTEGER PRIMARY KEY,
	typeId INTEGER,
	creatorId INTEGER,
	creationDate DATETIME DEFAULT (datetime('now','localtime')),

	word VARCHAR(50) UNIQUE,

	FOREIGN KEY (typeId) REFERENCES types(id),
	FOREIGN KEY (creatorId) REFERENCES users(id)
);
INSERT INTO words (typeId, creatorId, word)
       VALUES ((SELECT id FROM types WHERE types.type = 'cmavo'),
               (SELECT id FROM users WHERE users.username = 'kyrias'),
               "coi");
INSERT INTO words (typeId, creatorId, word)
       VALUES ((SELECT id FROM types WHERE types.type = 'gismu'),
               (SELECT id FROM users WHERE users.username = 'kyrias'),
               "cmene");
INSERT INTO words (typeId, creatorId, word)
       VALUES ((SELECT id FROM types WHERE types.type = 'cmavo'),
               (SELECT id FROM users WHERE users.username = 'kyrias'),
               "lo");



CREATE TABLE definitions (
	id INTEGER PRIMARY KEY,
	wordId INTEGER,
	languageId INTEGER,
	creatorId INTEGER,
	creationDate DATETIME,

	definition TEXT,

	notes TEXT,
	etymology TEXT,

	FOREIGN KEY (wordId) REFERENCES words(id),
	FOREIGN KEY (creatorId) REFERENCES users(id)
	FOREIGN KEY (languageId) REFERENCES languages(id)
);
INSERT INTO definitions (wordId, languageId, creatorId, creationDate, definition, notes)
       VALUES ((SELECT id FROM words WHERE words.word = "coi"),
               (SELECT id FROM languages WHERE languages.name = "English"),
               (SELECT id FROM users WHERE users.username = 'kyrias'),
               date('now'),
               "vocative: greetings/hello",
               "doi, rinsa");
INSERT INTO definitions (wordId, languageId, creatorId, creationDate, definition)
       VALUES ((SELECT id FROM words WHERE words.word = "coi"),
               (SELECT id FROM languages WHERE languages.name = "la lojban"),
               (SELECT id FROM users WHERE users.username = 'kyrias'),
               date('now'),
               "tcita lo cmene ja ve skicu le du'u sinxa le du'u makau te cusku .e le du'u rinsa le te cusku");



CREATE TABLE glosswords (
	id INTEGER PRIMARY KEY,

	glossword VARCHAR(50) UNIQUE
);
INSERT INTO glosswords (glossword)
       VALUES ("something");


CREATE TABLE definition_glosswords (
	definitionId INTEGER NOT NULL,
	glosswordId INTEGER NOT NULL,

	PRIMARY KEY (definitionId, glosswordId),
	FOREIGN KEY (definitionId) REFERENCES definitions(id),
	FOREIGN KEY (glosswordId) REFERENCES glosswords(id)
);
INSERT INTO definition_glosswords (definitionId, glosswordId)
       VALUES ((SELECT id FROM definitions WHERE definitions.wordId = (SELECT id FROM words WHERE words.word = "coi") AND definitions.languageId = 1),
               (SELECT id FROM glosswords WHERE glosswords.glossword = "something"));
INSERT INTO definition_glosswords (definitionId, glosswordId)
       VALUES ((SELECT id FROM definitions WHERE definitions.wordId = (SELECT id FROM words WHERE words.word = "coi") AND definitions.languageId = 2),
               (SELECT id FROM glosswords WHERE glosswords.glossword = "something"));
