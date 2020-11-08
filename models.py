from flask_login import UserMixin
from __init__ import app.db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document, UserMixin):
	email = db.StringField()
	password = db.StringField()

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, passwd):
		return check_password_hash(self.password, passwd)