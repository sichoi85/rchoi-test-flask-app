#!/usr/bin/env python
import os
import urllib.parse 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

# Configure Database URI: 
password = os.environ['password']
# Configure Database URI: 
params = urllib.parse.quote_plus("""Driver={ODBC Driver 17 for SQL Server};Server=tcp:rchoi-sql-server.database.windows.net,1433;Database=rchoi-db-v1;Uid=rchoidev;Pwd=%s;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;""" % (password))

# initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# extensions
db = SQLAlchemy(app)

class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	price = db.Column(db.Float, nullable=False)
	isbn = db.Column(db.Integer)

	def json(self):
		return {'name': self.name, 'price': self.price, 'isbn': self.isbn}

	def add_book(_name, _price, _isbn):
		new_book = Book(name=_name, price = _price, isbn = _isbn)
		db.session.add(new_book)
		db.session.commit()

	def get_all_books():
		return [Book.json(book) for book in Book.query.all()]

	def get_book(_isbn):
		return Book.query.filter_by(isbn=_isbn).first()

	def delete_book(_isbn):
		Book.query.filter_by(isbn=_isbn).delete()
		db.session.commit()

	def replace_book(_isbn, _name, _price):
		book_to_replace = Book.query.filter_by(isbn=_isbn).first()
		book_to_replace.name = _name
		book_to_replace.price = _price
		db.session.commit()

	def update_book_price(_isbn, _price):
		book_to_replace = Book.query.filter_by(isbn=_isbn).first()
		book_to_replace.price = _price
		db.session.commit()

	def update_book_name(_isbn, _name):
		book_to_replace = Book.query.filter_by(isbn=_isbn).first()
		book_to_replace.name = _name
		db.session.commit()

	def __repr__(self):
		book_object = {
			'name': self.name,
			'price': self.price,
			'isbn': self.isbn

		}
		return json.dumps(book_object)
