import os
import sqlite3

from flask import (
    Flask, g, redirect, render_template, request, session, url_for)


app = Flask(__name__)
app.secret_key = os.urandom(12)


def get_cursor():
    if 'db' not in g:
        g.db = sqlite3.connect('BDD_python_project.db')
    return g.db.cursor()


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


app.teardown_appcontext(close_db)


@app.route('/', methods=['GET', 'POST'])
def log():
    """Login page."""
    if request.method == 'POST':
        cursor = get_cursor()
        cursor.execute(
            "SELECT login, password FROM logs WHERE login=? AND password=?",
            (request.form['Login'], request.form['Password']))
        users = cursor.fetchall()

        if users:
            session['logged_in'] = True
            return render_template("Pages/Index.html")
        else:
            return render_template(
                'Pages/login.html', msgn="Mauvais User name ou Password !")

    return render_template('Pages/login.html')


@app.route('/createUser', methods=['GET', 'POST'])
def create():
    """Create a new user."""
    if request.method == 'POST':
        cursor = get_cursor()
        cursor.execute(
            "INSERT INTO logs (login, password) VALUES (?,?)",
            (request.form['newLogin'], request.form['newPassword']))
        cursor.connection.commit()
        return render_template('Pages/login.html', msgb="Utilisateur créé !")

    return render_template('Pages/nouvelUtilisateur.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('Pages/login.html')


@app.route('/Index')
def index():
    """Application index."""
    return render_template('Pages/Index.html')


@app.route('/Annuaire')
def Employe():
    cursor = get_cursor()
    cursor.execute("SELECT users_id, users_name, 'x', 'x' FROM USERS")
    donneesEmploye = cursor.fetchall()
    return render_template(
        'Pages/annuaire.html', donneesEmploye=donneesEmploye)


@app.route('/Crea', methods=['GET', 'POST'])
def Crea():
    """Team creation page where the user must enter the project name."""
    if request.method == 'POST':
        cursor = get_cursor()
        cursor.execute(
            'INSERT INTO PROJECTS (PROJECTS_name) VALUES (?)',
            (request.form['team_name'],))
        cursor.connection.commit()
        id_Project = cursor.lastrowid
        return redirect(url_for('choice', id_Project=id_Project))

    return render_template('Pages/Création_equipe.html')


@app.route('/choice/<int:id_Project>', methods=['GET', 'POST'])
def choice(id_Project):
    """Choice page when the user has validated the name of the team.

    Thanks to this page the user can adds members to the team previously
    created. Whenever an employee has been added to a team the page will
    regenerate. To leave this page, click on the end creation of a team that
    returns to the application index.

    """
    if request.method == 'POST':
        cursor = get_cursor()
        cursor.execute(
            "SELECT USERS_BY_PROJECT.USERS_ID FROM ("
            "RESPONSIBILITIES INNER JOIN ("
            "USERS INNER JOIN ("
            "SELECT USERS_BY_PROJECT.USERS_ID, "
            "Sum(USERS_BY_PROJECT.TIME) AS SBU "
            "FROM USERS LEFT JOIN USERS_BY_PROJECT "
            "ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID "
            "GROUP BY USERS_BY_PROJECT.USERS_ID, USERS.TAUX_HORAIRE) "
            "AS SU ON USERS.USERS_ID = SU.USERS_ID) "
            "ON RESPONSIBILITIES.Responsibilities_ID = "
            "USERS.Responsibilities_ID) "
            "LEFT JOIN USERS_BY_PROJECT "
            "ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID "
            "GROUP BY USERS_BY_PROJECT.USERS_ID, "
            "[USERS].[TAUX_HORAIRE]-SU.SBU, "
            "RESPONSIBILITIES.Responsibilities_Name "
            "HAVING (((RESPONSIBILITIES.Responsibilities_Name)=?)) "
            "ORDER BY [USERS].[TAUX_HORAIRE]-SU.SBU DESC;",
            (request.form['ROLES'],))
        x = cursor.fetchall()
        x2 = x[0]
        user_select = x2[0]

        cursor.execute(
            "INSERT INTO USERS_BY_PROJECT (TIME,USERS_ID,PROJECTS_ID) "
            "VALUES (?,?,?)", (request.form['TIME'], user_select, id_Project))
        cursor.connection.commit()

        return render_template(
            'Pages/choice.html', id_Project=id_Project, msgv=(
                "Employé Ajouté ! Vous pouvez continuer ou valide votre "
                "equipe en cliquant sur fin création d'equipe"))

    return render_template('Pages/choice.html', id_Project=id_Project)


@app.route('/Equipe')
def Equipe():
    """Current projects and users linked to the different projects."""
    cursor = get_cursor()
    cursor.execute(
        "SELECT USERS_BY_PROJECT.USERS_ID,USERS.USERS_NAME,"
        "USERS_BY_PROJECT.PROJECTS_ID,PROJECTS.PROJECTS_name,"
        "USERS_BY_PROJECT.TIME FROM PROJECTS "
        "INNER JOIN ("
        "USERS INNER "
        "JOIN USERS_BY_PROJECT ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID) "
        "ON PROJECTS.PROJECTS_ID = USERS_BY_PROJECT.PROJECTS_ID "
        "LIMIT 200 OFFSET 14")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM PROJECTS WHERE PROJECTS_ID > 1")
    equipe = cursor.fetchall()

    return render_template(
        'Pages/Equipe_cree.html', Equipe=equipe, Users=users)


@app.route('/Delete', methods=['GET', 'POST'])
def Delete():
    """Delete a project according to the project id."""
    if request.method == 'POST':
        if request.form['id'] == '1':
            return render_template(
                'Pages/Delete.html', msg="Impossible de suprrimé cette valeur")
        cursor = get_cursor()
        cursor.execute(
            "DELETE FROM PROJECTS WHERE PROJECTS_ID = ?",
            (request.form['id'],))
        cursor.execute(
            "DELETE FROM USERS_BY_PROJECT WHERE PROJECTS_ID = ?",
            (request.form['id'],))
        cursor.connection.commit()
        return render_template('Pages/Delete.html', msg=(
            "Equipe supprimé ! Vous pouvez continuer ou utilisé le menu "
            "ci dessus pour d'autres fonctionnalités"))

    return render_template('Pages/Delete.html')
