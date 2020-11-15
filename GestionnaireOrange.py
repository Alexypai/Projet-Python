from flask import Flask, render_template, request, redirect, url_for, flash, request, session, abort
import sqlite3
import os

db_local = 'BDD_python_project.db'

app = Flask(__name__)

norepeat = []

app.secret_key = os.urandom(12)

@app.route('/', methods = ['GET', 'POST'])
def log():
    session['logged_in'] = True
    if request.method == 'GET':
        return render_template('Pages/login.html')
    else:
        log_user = (
            request.form['Login']
        )
        password_user = (
            request.form['Password']
        )
        connexion(log_user, password_user)
        v = connexion(log_user, password_user)
    
    if v == True:
        return render_template("Pages/Index.html")
    else:
        return render_template('Pages/login.html')

def connexion(log_user, password_user):
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("SELECT login, password FROM logs WHERE login=? AND password=?",(log_user,password_user))
    id = c.fetchall()
    if not id == False:
        validation = False
    else:
        id2 = id[0]
        idu = id2[0]
        idp = id2[1]
        connect.close()
        if ((password_user == idp) and (log_user == idu)):
            validation = True
        else:
            validation = False
    return(validation)


@app.route('/createUser', methods = ['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('Pages/nouvelUtilisateur.html')
    else:
        new_log_user = (
            request.form['newLogin']
        )
        new_password_user = (
            request.form['newPassword']
        )
        newUser(new_log_user, new_password_user)
        return render_template('Pages/login.html')

def newUser(new_log_user,new_password_user):
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("INSERT INTO logs (login, password) VALUES (?,?)",(new_log_user,new_password_user))
    connect.commit()
    connect.close()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('Pages/login.html')

@app.route('/Index')
def index():
    id_Project = None
    print(id_Project)
    return render_template('Pages/Index.html')

@app.route('/Annuaire')
def Annuaire():
    return render_template('Pages/Annuaire.html')

@app.route('/Crea', methods = ['GET','POST'])
def Crea():
    if request.method == 'GET':
        return render_template('Pages/Création_equipe.html')
    else:
        new_team = (
            request.form['team_name']
        )
        insert_team(new_team)
        return redirect(url_for('choice'))


def insert_team(new_team):
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    sql_team_write = 'INSERT INTO PROJECTS (PROJECTS_name) VALUES (?)'
    c.execute(sql_team_write,[new_team])
    connect.commit()
    c2 = connect.cursor()
    c2.execute("SELECT PROJECTS_ID FROM PROJECTS WHERE PROJECTS_name=?",(new_team,))
    x = c2.fetchone()
    global id_Project
    id_Project = x[0]
    connect.close()

@app.route('/Equipe')    
def Equipe():
    Equipe = query_equipe()
    Users = query_users()
    return render_template('Pages/Equipe_cree.html',Equipe=Equipe,Users=Users)

def query_equipe():
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("SELECT * FROM PROJECTS")
    Users = c.fetchall()
    connect.close()
    return Users

def query_users():
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("SELECT USERS_BY_PROJECT.USERS_ID,USERS.USERS_NAME,USERS_BY_PROJECT.PROJECTS_ID,PROJECTS.PROJECTS_name,USERS_BY_PROJECT.TIME FROM PROJECTS INNER JOIN (USERS INNER JOIN USERS_BY_PROJECT ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID) ON PROJECTS.PROJECTS_ID =  USERS_BY_PROJECT.PROJECTS_ID")
    Equipe = c.fetchall()
    connect.close()
    return Equipe

@app.route('/choice', methods = ['GET','POST'])
def choice():
    if request.method == 'GET':
        return render_template('Pages/choice.html')
    else:
        time_user = (
            request.form['TIME']
        )
        role_user = (
            request.form['ROLES']
        )
        insert_user(id_Project,time_user, role_user)
        return redirect(url_for('choice'))

def insert_user(id_Project,time_user, role_user):
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("SELECT USERS_BY_PROJECT.USERS_ID FROM (RESPONSIBILITIES INNER JOIN (USERS INNER JOIN (SELECT USERS_BY_PROJECT.USERS_ID, Sum(USERS_BY_PROJECT.TIME) AS SBU FROM USERS LEFT JOIN USERS_BY_PROJECT ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID GROUP BY USERS_BY_PROJECT.USERS_ID, USERS.TAUX_HORAIRE)  AS SU ON USERS.USERS_ID = SU.USERS_ID) ON RESPONSIBILITIES.Responsibilities_ID = USERS.Responsibilities_ID) LEFT JOIN USERS_BY_PROJECT ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID GROUP BY USERS_BY_PROJECT.USERS_ID, [USERS].[TAUX_HORAIRE]-SU.SBU, RESPONSIBILITIES.Responsibilities_Name HAVING (((RESPONSIBILITIES.Responsibilities_Name)=?)) ORDER BY [USERS].[TAUX_HORAIRE]-SU.SBU DESC;",(role_user,))
    x = c.fetchall()
    x2 = x[0]
    user_select = x2[0]
    print(user_select)
    if not norepeat:
        norepeat.append(user_select)
    else:
         for i in range(len(norepeat)):
            if norepeat[i] == user_select:
                x2 = x[0]
                user_select = x2[i+1]
                print(user_select)
    c2 = connect.cursor()
    c2.execute("INSERT INTO USERS_BY_PROJECT (TIME,USERS_ID,PROJECTS_ID) VALUES (?,?,?)",(time_user,user_select,id_Project))
    connect.commit()
    connect.close()

@app.route('/Delete', methods = ['GET','POST'])
def Delete():
    if request.method == 'GET':
        return render_template('Pages/Delete.html')
    else:
        team_id = (
            request.form['id']
        )
        delete_team(team_id)
        return redirect(url_for('Delete'))

def delete_team(team_id):
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("DELETE FROM PROJECTS WHERE PROJECTS_ID = ?",(team_id,))
    connect.commit()
    c.execute("DELETE FROM USERS_BY_PROJECT WHERE PROJECTS_ID = ?",(team_id,))
    connect.commit()
    connect.close()



   











































































































































