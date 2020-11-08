import sqlite3

from flask import Flask, render_template
from flask_mongoengine import MongoEngine

db_locale = 'app.db'

connie = sqlite3.connect(db_locale)

app = Flask(__name__)

engine = create_engine ( 'sqlite: app.db' , echo = True )

# créer une session
Session = sessionmaker (bind = engine) 
session = Session ()

user = User ( "admin" , "password" ) 
session.add (user)

user = User ( "python" , "python" ) 
session.add (utilisateur)

user = User ( "Flavien" , "python" ) 
session.add (user)

# valider l'enregistrement de la base de données
session.commit ()

session.commit ()

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404