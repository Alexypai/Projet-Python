-- CREATE TABLES 

DROP TABLE IF EXISTS RESPONSIBILITIES;
DROP TABLE IF EXISTS PROJECTS;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS USERS_BY_PROJECT;

CREATE TABLE RESPONSIBILITIES (
Responsibilities_ID INTEGER PRIMARY KEY AUTOINCREMENT,
Responsibilities_Name text not null);
CREATE TABLE USERS (
    USERS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERS_NAME text NOT NULL,
    TAUX_HORAIRE INTEGER NOT NULL,
    BIRTHDAY text NOT NULL,
    CONTACT_MAIL text NOT NULL,
    CONTACT_NUMBER INTEGER,
    ENTITY text NOT NULL,
    Responsibilities_ID,
        FOREIGN KEY (Responsibilities_ID)
            REFERENCES RESPONSIBILITIES (Responsibilities_ID)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
CREATE TABLE PROJECTS (
    PROJECTS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PROJECTS_name text NOT NULL);
CREATE TABLE USERS_BY_PROJECT (
    UP_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TIME INTEGER NOT NULL,
    USERS_ID,
    PROJECTS_ID,
    FOREIGN KEY (USERS_ID)
            REFERENCES USERS (USERS_ID)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
    FOREIGN KEY (PROJECTS_ID)
            REFERENCES PROJECTS (PROJECTS_ID)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);

CREATE TABLE logs(
logs_ID INTEGER PRIMARY KEY AUTOINCREMENT,
login text not null,
password text not null);

-- DATA + INIT VALUE 

INSERT INTO RESPONSIBILITIES (Responsibilities_Name)
VALUES ("RH"),("MANAGER"),("DEVELOPER"),("ASSISTANT"),("COMMERCIAL");

INSERT INTO USERS (USERS_NAME,TAUX_HORAIRE,BIRTHDAY,CONTACT_MAIL,CONTACT_NUMBER,ENTITY,Responsibilities_ID)
VALUES ("Féret","35","01/02/1988","Féret@orange.com","600203554","Orange/OF/DTSI/DTRS/UPRSE/ID2R/GOP","1"),
('Gide','20','11/06/1980','Gide@orange.com','615483554','Orange/OF/DTSI/DTRS/UPRNE/ID2R',"2"),
('Vaillancourt','30','19/12/1990','Vaillancourt@orange.com','600201975','Orange/OF/DTSI/DTRS/UPRSE',"3"),
('Laurens','40','31/07/1978','Laurens@orange.com','604723554','Orange/OF',"2"),
('Benett','15','01/02/2000','Benett@orange.com','614586354','Orange/OF/DTSI/DTRS/UPRSE/ID2R',"4"),
('Alméras','27','25/10/1970','Alméras@orange.com','789303554','Orange/OF/DTSI/DTRS',"5"),
('Charbonneau','30','01/04/1995','Charbonneau@orange.com','600147854','Orange/OF/DTSI/DTRS/UPRSE/ID2R/GOP',"3"),
('Bullion','35','22/02/1969','Bullion@orange.com','614523654','Orange/OF/DTSI',"1"),
('Dumont','20','19/08/1992','Dumont@orange.com','645693554','Orange/OF/DTSI/DTRS/UPRSE/ID2R/GOP',"4"),
('Lussier','40','25/01/1997','Lussier@orange.com','614783654','Orange/OF/DTSI/DTRS',"5"),
('Cazenave','29','04/05/1970','Cazenave@orange.com','789303554','Orange/OF/DTSI/DTRS',"5"),
('Génin','45','30/06/1982','Génin@orange.com','600185254','Orange/OF/DTSI/DTRS/UPRSE/ID2R/GOP',"3"),
('Leclère','17','23/02/1999','Leclère@orange.com','756423654','Orange/OF/DTSI',"4"),
('Beauchamp','30','19/11/1962','Beauchamp@orange.com','645691487','Orange/OF/DTSI/DTRS/UPRSE',"2");

INSERT INTO USERS_BY_PROJECT (TIME,USERS_ID,PROJECTS_ID)
VALUES 
(0,2,"1"),
(0,3,"1"),
(0,4,"1"),
(0,5,"1"),
(0,6,"1"),
(0,7,"1"),
(0,8,"1"),
(0,9,"1"),
(0,10,"1"),
(0,11,"1"),
(0,12,"1"),
(0,13,"1"),
(0,14,"1"),
(0,15,"1");


INSERT INTO logs (login, password) VALUES (600203554, 1231);
INSERT INTO logs (login, password) VALUES (615483554, 1232);
INSERT INTO logs (login, password) VALUES (600201975, 1233);
INSERT INTO logs (login, password) VALUES (604723554, 1234);
INSERT INTO logs (login, password) VALUES (614586354, 1235);
INSERT INTO logs (login, password) VALUES (789303554, 1236);
INSERT INTO logs (login, password) VALUES (600147854, 1237);
INSERT INTO logs (login, password) VALUES (614523654, 1238);
INSERT INTO logs (login, password) VALUES (645693554, 1239);
INSERT INTO logs (login, password) VALUES (614783654, 1241);
INSERT INTO logs (login, password) VALUES (789303554, 1242);
INSERT INTO logs (login, password) VALUES (600185254, 1243);
INSERT INTO logs (login, password) VALUES (756423654, 1244);
INSERT INTO logs (login, password) VALUES (645691487, 1245);