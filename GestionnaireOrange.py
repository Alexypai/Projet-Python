from flask import Flask, render_template, request, redirect, url_for,session, abort,flash
import sqlite3

#Variable correspondant a la base de donnée de l'application
db_local = 'BDD_python_project.db'

app = Flask(__name__)

norepeat = []


#Index de l'application avec mise a zero de la variable id_project lorsqu'un utilisateur a fini de crée une équipe  
@app.route('/')
def index():
    id_Project = None
    print(id_Project)
    return render_template('Pages/Index.html')

@app.route('/Annuaire')
def Annuaire():
    return render_template('Pages/Annuaire.html')

# renvoie la page de création d'equipe ou l'utilisateur doit entrée le nom du projet
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

#Fonction permettant l'ajout du projet nommé dans la page création d'equipe et attribue un id a ce nouveau projet
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

#Affichage de la page "choice" lorsque l'utilisateur a validé le nom de l'equipe,
#Grace a cette page l'utilisateur rajoute des membres a l'equipe précedement créé
# (Chaque fois qu'un employé a été ajoute a une equipe la page se regenere, 
# pour quitter cette page il faut cliqué sur fin creation d'equipe qui renvoie sur l'index de l'application.
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
        msgv = msgA()
        return render_template('Pages/choice.html',msgv=msgv)

#fonction permettant l'ajout d'un employé ayant le plus de temps disponble dans l'equipe précedement crée, selon le role chosit par l'utilisateur
# Lors de l'ajout, cette fonction insere dans la table USERS_BY_PROJECT : l'id de l'employé ayant le plus de temps disponible, l'id du projet précedement crée et le temps qu'il lui a été attribué.
def insert_user(id_Project,time_user, role_user):
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("SELECT USERS_BY_PROJECT.USERS_ID FROM (RESPONSIBILITIES INNER JOIN (USERS INNER JOIN (SELECT USERS_BY_PROJECT.USERS_ID, Sum(USERS_BY_PROJECT.TIME) AS SBU FROM USERS LEFT JOIN USERS_BY_PROJECT ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID GROUP BY USERS_BY_PROJECT.USERS_ID, USERS.TAUX_HORAIRE)  AS SU ON USERS.USERS_ID = SU.USERS_ID) ON RESPONSIBILITIES.Responsibilities_ID = USERS.Responsibilities_ID) LEFT JOIN USERS_BY_PROJECT ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID GROUP BY USERS_BY_PROJECT.USERS_ID, [USERS].[TAUX_HORAIRE]-SU.SBU, RESPONSIBILITIES.Responsibilities_Name HAVING (((RESPONSIBILITIES.Responsibilities_Name)=?)) ORDER BY [USERS].[TAUX_HORAIRE]-SU.SBU DESC;",(role_user,))
    x = c.fetchall()
    x2 = x[0]
    user_select = x2[0]
    print(user_select)
    #Si ll'utilisateru a besoin de 2RH par exemple grace a cette condition, la fonction n'ajoute pas 2fois la meme personne au meme projet
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

def msgA():
    msgV = "Employé Ajouté ! Vous pouvez continuer ou valide votre equipe en cliquant sur fin création d'equipe"
    return msgV

def msgD():
    msgV = "Equipe supprimé ! Vous pouvez continuer ou utilisé le menu ci dessus pour d'autres fonctionnalités"
    return msgV


#permet de voir toutes les projets en cours et les utilisateurs rattaché aux differents projets
@app.route('/Equipe')    
def Equipe():
    Equipe = query_equipe()
    Users = query_users()
    return render_template('Pages/Equipe_cree.html',Equipe=Equipe,Users=Users)

#Selectionne tous les données de la tables PROJETCS
def query_equipe():
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("SELECT * FROM PROJECTS")
    Users = c.fetchall()
    connect.close()
    return Users

#Selectione toutes les données de la table USERS
def query_users():
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("SELECT USERS_BY_PROJECT.USERS_ID,USERS.USERS_NAME,USERS_BY_PROJECT.PROJECTS_ID,PROJECTS.PROJECTS_name,USERS_BY_PROJECT.TIME FROM PROJECTS INNER JOIN (USERS INNER JOIN USERS_BY_PROJECT ON USERS.USERS_ID = USERS_BY_PROJECT.USERS_ID) ON PROJECTS.PROJECTS_ID =  USERS_BY_PROJECT.PROJECTS_ID")
    Equipe = c.fetchall()
    connect.close()
    return Equipe


#Permet a l'utilisateur de supprimé un projet selon l'id du projet
@app.route('/Delete', methods = ['GET','POST'])
def Delete():
    if request.method == 'GET':
        return render_template('Pages/Delete.html')
    else:
        team_id = (
            request.form['id']
        )
        delete_team(team_id)
        msg = msgD()
        return render_template('Pages/Delete.html',msg=msg)

#Permet la suppresion d'un projet dans la table PROJECT
def delete_team(team_id):
    connect = sqlite3.connect(db_local)
    c = connect.cursor()
    c.execute("DELETE FROM PROJECTS WHERE PROJECTS_ID = ?",(team_id,))
    connect.commit()
    c.execute("DELETE FROM USERS_BY_PROJECT WHERE PROJECTS_ID = ?",(team_id,))
    connect.commit()
    connect.close()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=4000)



   











































































































































