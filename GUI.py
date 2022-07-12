from ast import main
from calendar import c
from cgitb import text
from sqlite3 import Row
from tkinter import *
from tkinter.tix import COLUMN
from turtle import width 
from PIL import ImageTk, Image
import psycopg2
from config import config
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

root = Tk()
root.title('Formation Continue')
root.geometry("600x500")

def connect():
    #Connecting to PostgreSQL server
    conn = None
    try:
        #Reading the conncetion parameters
        params = config()

        #Connecting to the postgresql server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        #Creating a cursor to be able to execute functions
        cur = conn.cursor()

        #Executing a statement to get the version of the database
        print('PostgreSQL database version: ')
        cur.execute('select version()')

        #Printing the version of the database
        db_version = cur.fetchone()
        print(db_version)

        #Closing the communication with PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    connect()



#Creating some functions

#This function is made to clear the fields when the button "Supprimer les valeurs" is clicked
def supprimer_valeurs():
    Nom_Box.delete(0, END)
    Prenom_Box.delete(0, END)
    Telephone_Box.delete(0, END)
    Email_Box.delete(0, END)
    Niveau_Etudes_Box.delete(0, END)
    Fonction_Box.delete(0, END)
    Commune_Box.delete(0, END)
    Souhait_Box.delete(0, END)
    Domaine_box.delete(0, END)
    Besoin_box.delete(0, END)
    


def ajouter_elu():
    #Here, we're extracting the Id of "domaine" from the string present in the combo box
    domaine_id = Domaine_box.get()[0]
    #Same thing for "besoin"
    besoin_id = Besoin_box.get()[0]
    #And finally, we do the same thing for commune
    commune_id = Commune_Box.get()[0]
    #To get the name of "la commune" only from the "Commune" combo box, we strip out the first three characters.
    #For example, if the first commune is "1. Rabat", we split out the first three characters 
    Commune = Commune_Box.get()
    Commune = Commune[3:]
    #We do the same thing for "Niveau d'études"
    niveau_etudes = Niveau_Etudes_Box.get()
    niveau_etudes = niveau_etudes[3:]
    #Creating the sql command
    sql = "insert into elu(elu_nom, elu_prenom, elu_telephone, elu_email, elu_niveau_etudes, elu_fonction, elu_commune, elu_souhait, domaine_id, besoin_id, commune_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (Nom_Box.get(), Prenom_Box.get(), Telephone_Box.get(), Email_Box.get(), niveau_etudes, Fonction_Box.get(), Commune, Souhait_Box.get(), domaine_id, besoin_id, commune_id)
    conn = None
    try: 
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    supprimer_valeurs()

def retour_au_menu_principal():
    global root
    root.destroy()
    root = Tk()
    
    


title_label = Label(root, text = "Ajouter les informations d'un élu à la base de données", font=("Helvetica", 16))
title_label.grid(row = 0, column = 0, columnspan = 2, pady = 30, padx=35)

#Putting up the fields
Nom = Label(root, text = "Nom").grid(row = 1, column=0, sticky = W, padx=10, pady=3)
Prenom = Label(root, text = "Prenom").grid(row = 2, column=0, sticky = W, padx=10, pady=3)
Telephone = Label(root, text="Telephone").grid(row=3, column=0, sticky = W, padx=10, pady=3)
Email = Label(root, text="Email").grid(row=4, column=0, sticky=W, padx=10, pady=3)
Niveau_Etudes = Label(root, text="Niveau d'études").grid(row=5, column=0, sticky = W, padx=10, pady=3)
Fonction = Label(root, text="Fonction").grid(row=6, column=0, sticky = W, padx=10, pady=3)
Commune = Label(root, text="Commune").grid(row=7, column=0, sticky = W, padx=10, pady=3)
Souhait = Label(root, text="Souhait").grid(row=8, column=0, sticky = W, padx=10, pady=3)
Domaine = Label(root, text="Domaine").grid(row=9, column=0, sticky=W, padx=10, pady=3)
Besoin = Label(root, text="Besoin").grid(row=10, column=0, sticky=W, padx=10, pady=3)




#Putting up the input boxes
Nom_Box = Entry(root, width=30)
Nom_Box.grid(row = 1, column=1, pady=5)

Prenom_Box = Entry(root, width=30)
Prenom_Box.grid(row=2, column=1, pady=5)

Telephone_Box = Entry(root, width=30)
Telephone_Box.grid(row=3, column=1, pady = 5)

Email_Box = Entry(root, width=30)
Email_Box.grid(row=4, column=1, pady=5)

Niveau_Etudes_Box = ttk.Combobox(root, value=["", "1. Néant", "2. Primaire", "3. Collège", "4. Lycée", "5. Institut Technique", "6. Universitaire", "7. Supérieur"], width=27)
Niveau_Etudes_Box.current(0)
Niveau_Etudes_Box.grid(row=5, column=1, pady=5)

Fonction_Box = Entry(root, width=30)
Fonction_Box.grid(row=6, column=1, pady=5)

Commune_Box = ttk.Combobox(root, value=["", "1. Rabat", "2. Temara", "3. Tamesna", "4. Sale", "5. Sale El Jadida", "6. Khmissat"], width=27)
Commune_Box.current(0)
Commune_Box.grid(row=7, column=1, pady=5)

Souhait_Box = Entry(root, width=30)
Souhait_Box.grid(row=8, column=1, pady=5)
#Combo box for "Domaine" and "Besoin"
Domaine_box = ttk.Combobox(root, value=["", "1. Urbanisme", "2. Finances", "3. Police Administrative", "4. Etat civil", "5. Environnement", "6. Transport Public", "7. Planification Stratégique"], width=27)
Domaine_box.current(0)
Domaine_box.grid(row=9, column=1, pady=5)

Besoin_box = ttk.Combobox(root, value=["", "1. Urbanisme", "2. Finances", "3. Police Administrative", "4. Etat civil", "5. Environnement", "6. Transport Public", "7. Planification Stratégique"], width=27)
Besoin_box.current(0)
Besoin_box.grid(row=10, column=1, pady=5)


#Creating Buttons
Ajouter_Elu = Button(root, text="Ajouter cet élu à la base de données", command=ajouter_elu)
Ajouter_Elu.grid(row = 11, column=0, padx=10, pady=15)

Supprimer_Valeurs = Button(root, text="Supprimer les valeurs", command=supprimer_valeurs)
Supprimer_Valeurs.grid(row = 11, column=1)

Retour_Menu_Principal = Button(root, text="Retourner au Menu Principal", command=retour_au_menu_principal)
Retour_Menu_Principal.grid(row = 12, column=0) 

root.mainloop()