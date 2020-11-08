from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email

class LoginForm(Form):
	email = TextField('', [Email(), Required(
		message='Mauvaise adresse mail')], default="my@fra.com",
	)
	password = PasswordField('', [Required(
		message='Mauvais mot de passe')], default="fra", render_kw={"placeholder": "Password"}
	)