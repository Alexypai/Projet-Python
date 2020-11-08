import sqlite3

from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_login import LoginManager

db_locale = 'app.db'

connie = sqlite3.connect(db_locale)

app = Flask(__name__)

# Config
app.config.from_object('config')

# Database init
db = 'app.db'

# Login Management
login_manager = LoginManager()
login_manager.login_view = "/admin/login/"
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module
from views.mod_adm.views import mod_adm as adm_module
from views.mod_adm.views import AdminCustomView, UserView, MealView
from views.mod_adm.models import User, Meal

# Register blueprint(s)
app.register_blueprint(adm_module, url_prefix='/admin')

# Init admin
admin = Admin(name='Admin', template_mode='', index_view=AdminCustomView())
admin.init_app(app)