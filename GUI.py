from ast import main
from calendar import c
from cgitb import text
from textwrap import TextWrapper, wrap
from tkinter import *
from tkinter.tix import COLUMN
from tokenize import cookie_re
from turtle import width
from unittest import result
from unittest.util import _count_diff_all_purpose 
from PIL import ImageTk, Image
import psycopg2
from config import config
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import csv

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
    afficher_menu_principal()


def afficher_menu_principal():
    global root
    root = Tk()
    root.geometry("600x650")
    root.title("Formation Continue")
    #Putting up the title 
    menu_principal_titre = Label(root, text = "Formation Continue: Menu Principal\nQue souhaitez vous faire?", font = ("Helvetica", 16), bd=4)
    menu_principal_titre.grid(row=0, column=0, columnspan=2, padx=140, pady=25)

    #Putting up labels and buttons on the left 
    Elu_Label = Label(root, text="Concernant les élus:", font=("Helvetica", 14))
    Elu_Label.grid(row=1, column=0, padx=10, pady=25)

    Ajouter_Elu_Button = Button(root, text="Ajouter un élu à la base de données", command=ajouter_elu_interface,)
    Ajouter_Elu_Button.grid(row=2, column=0, padx=10, pady=25)

    Rechercher_Elu_Button = Button(root, text="Rechercher un élu", command=rechercher_elu_interface)
    Rechercher_Elu_Button.grid(row=3, column=0, padx=10, pady=25)

    Changer_Elu_Button = Button(root, text="Changer les informations d'un élu")
    Changer_Elu_Button.grid(row=4, column=0, padx=10, pady=25)

    Supprimer_Elu_Button = Button(root, text="Supprimer les informations d'un élu")
    Supprimer_Elu_Button.grid(row=5, column=0, padx=10, pady=25)

    Afficher_Elus_Button = Button(root, text="Afficher tous les élus", command=afficher_elus_interface)
    Afficher_Elus_Button.grid(row=6, column=0, padx=10, pady=25)

    #And on the right
    Formation_Label = Label(root, text="Concernant les formations:", font=("Helvetica", 14))
    Formation_Label.grid(row=1, column=1, padx=10, pady=25)

    Ajouter_Formation_Button = Button(root, text="Ajouter une formation à la base de données")
    Ajouter_Formation_Button.grid(row=2, column=1, padx=10, pady=25)

    Rechercher_Formation_Button = Button(root, text="Rechercher une formation")
    Rechercher_Formation_Button.grid(row=3, column=1, padx=10, pady=25)

    Changer_Formation_Button = Button(root, text="Changer les informations d'une formation")
    Changer_Formation_Button.grid(row=4, column=1, padx=10, pady=25)

    Supprimer_Formation_Button = Button(root, text="Supprimer les informations d'une formation")
    Supprimer_Formation_Button.grid(row=5, column=1, padx=10, pady=25)

    Afficher_Formation_Button = Button(root, text="Afficher toutes les formations")
    Afficher_Formation_Button.grid(row=6, column=1, padx=10, pady=25)

    #Adding a label and a button in the center
    Fonctions_Label = Label(root, text="Autres:", font=("Helvetica", 14))
    Fonctions_Label.grid(row=7, column=0, columnspan=2)

    Fonctions_Button = Button(root, text="Utiliser les fonctions statistiques")
    Fonctions_Button.grid(row=8, column=0, columnspan=2, pady=25)



    root.mainloop()
    
    
    

def ajouter_elu_interface():
    global root
    root.destroy()
    root = Tk()
    root.title('Formation Continue')
    root.geometry("600x500")
    title_label = Label(root, text = "Ajouter les informations d'un élu à la base de données", font=("Helvetica", 16))
    title_label.grid(row = 0, column = 0, columnspan = 2, pady = 30, padx=35)

    #Putting up the fields
    Nom = Label(root, text = "Nom")
    Nom.grid(row = 1, column=0, sticky = W, padx=10, pady=3)
    Prenom = Label(root, text = "Prenom")
    Prenom.grid(row = 2, column=0, sticky = W, padx=10, pady=3)
    Telephone = Label(root, text="Telephone")
    Telephone.grid(row=3, column=0, sticky = W, padx=10, pady=3)
    Email = Label(root, text="Email")
    Email.grid(row=4, column=0, sticky=W, padx=10, pady=3)
    Niveau_Etudes = Label(root, text="Niveau d'études")
    Niveau_Etudes.grid(row=5, column=0, sticky = W, padx=10, pady=3)
    Fonction = Label(root, text="Fonction")
    Fonction.grid(row=6, column=0, sticky = W, padx=10, pady=3)
    Commune = Label(root, text="Commune")
    Commune.grid(row=7, column=0, sticky = W, padx=10, pady=3)
    Souhait = Label(root, text="Souhait")
    Souhait.grid(row=8, column=0, sticky = W, padx=10, pady=3)
    Domaine = Label(root, text="Domaine")
    Domaine.grid(row=9, column=0, sticky=W, padx=10, pady=3)
    Besoin = Label(root, text="Besoin")
    Besoin.grid(row=10, column=0, sticky=W, padx=10, pady=3)




    #   Putting up the input boxes
    global Nom_Box
    Nom_Box = Entry(root, width=30)
    Nom_Box.grid(row = 1, column=1, pady=5)

    global Prenom_Box
    Prenom_Box = Entry(root, width=30)
    Prenom_Box.grid(row=2, column=1, pady=5)

    global Telephone_Box
    Telephone_Box = Entry(root, width=30)
    Telephone_Box.grid(row=3, column=1, pady = 5)

    global Email_Box
    Email_Box = Entry(root, width=30)
    Email_Box.grid(row=4, column=1, pady=5)

    global Niveau_Etudes_Box
    Niveau_Etudes_Box = ttk.Combobox(root, value=["", "1. Néant", "2. Primaire", "3. Collège", "4. Lycée", "5. Institut Technique", "6. Universitaire", "7. Supérieur"], width=27)
    Niveau_Etudes_Box.current(0)
    Niveau_Etudes_Box.grid(row=5, column=1, pady=5)

    global Fonction_Box
    Fonction_Box = Entry(root, width=30)
    Fonction_Box.grid(row=6, column=1, pady=5)

    global Commune_Box
    Commune_Box = ttk.Combobox(root, value=["", "1. Rabat", "2. Temara", "3. Tamesna", "4. Sale", "5. Sale El Jadida", "6. Khmissat"], width=27)
    Commune_Box.current(0)
    Commune_Box.grid(row=7, column=1, pady=5)

    global Souhait_Box
    Souhait_Box = Entry(root, width=30)
    Souhait_Box.grid(row=8, column=1, pady=5)
    #Combo box for "Domaine" and "Besoin"
    global Domaine_box
    Domaine_box = ttk.Combobox(root, value=["", "1. Urbanisme", "2. Finances", "3. Police Administrative", "4. Etat civil", "5. Environnement", "6. Transport Public", "7. Planification Stratégique"], width=27)
    Domaine_box.current(0)
    Domaine_box.grid(row=9, column=1, pady=5)

    global Besoin_box
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




#Interface pour chercher un élu spécifique par nom de famille
def rechercher_elu_interface():
    global root
    root.destroy()
    root = Tk()
    root.title('Formation Continue')
    root.geometry("1050x600")

    def chercher_elu():
        global sql 
        global result 
        selected = drop.get()
        if selected == "Rechercher par...":
            label = Label(root, text="Veuillez Sélectionner une Catégorie de Recherche")
            label.grid(row=3, column=1)
            result = not result
        if selected == "Nom de Famille":
            sql = "Select elu_id, elu_nom, elu_prenom, elu_telephone, elu_email, elu_niveau_etudes, elu_fonction, elu_souhait from elu where elu_nom = %s"
        if selected == "Email":
            sql = "Select elu_id, elu_nom, elu_prenom, elu_telephone, elu_email, elu_niveau_etudes, elu_fonction, elu_souhait from elu where elu_email = %s"
        if selected == "Numéro (Id)":
            sql = "Select elu_id, elu_nom, elu_prenom, elu_telephone, elu_email, elu_niveau_etudes, elu_fonction, elu_souhait from elu where elu_id = %s"
        conn = None
        searched = search_box.get()
        name = (searched, )
        try:
            params = config() 
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, name)
            result = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        if not result:
            result = "Elu non Trouvé..."
            #Putting up the result on the screen
            searched_label = Label(root, text=result)
            searched_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        else:
            Id_Label = Label(root, text="Numéro (Id)", font=("Helvetica, 14"))
            Id_Label.grid(row=2, column=0)
            Nom_Label = Label(root, text="Nom", font=("Helvetica, 14"))
            Nom_Label.grid(row=2, column=1)
            Prenom_Label = Label(root, text="Prenom", font=("Helvetica, 14"))
            Prenom_Label.grid(row=2, column=2)
            Telephone_Label = Label(root, text="Telephone", font=("Helvetica, 14"))
            Telephone_Label.grid(row=2, column=3)
            Email_Label = Label(root, text="Email", font=("Helvetica, 14"))
            Email_Label.grid(row=2, column=4)
            Niveau_Etudes_Label = Label(root, text="Niveau d'études", font=("Helvetica, 14"))
            Niveau_Etudes_Label.grid(row=2, column=5)
            Fonction_Label = Label(root, text="Fonction", font=("Helvetica, 14"))
            Fonction_Label.grid(row=2, column=6)
            Souhait_Label = Label(root, text="Souhait", font=("Helvetica, 14"))
            Souhait_Label.grid(row=2, column=7)

            for index, i in enumerate(result):
                num = 0
                index += 3
                for y in i:
                    elu_label = Label(root, text=y)
                    elu_label.grid(row=index, column=num, pady=15, padx=5)
                    num += 1
            csv_button = Button(root, text="Exporter vers Excel", command=lambda: export_to_csv(result))
            csv_button.grid(row=index + 1, column=0)
        

    #Label
    search_label = Label(root, text="Rechercher un élu")
    search_label.grid(row=0, column=0, padx=10, pady=10)
    #Entry box pour entrer le nom de famille
    search_box = Entry(root)
    search_box.grid(row=0, column=1, padx=10, pady=10)
    #Bouton pour rechercher
    search_button = Button(root, text="Chercher élu", command=chercher_elu)
    search_button.grid(row=1, column=0, padx=10, pady=10)
    #Drop down Box
    drop = ttk.Combobox(root, value=["Rechercher par...", "Nom de Famille", "Email", "Numéro (Id)"])
    drop.current(0)
    drop.grid(row = 0, column=2)
    Retour_Menu_Principal = Button(root, text="Retourner au Menu Principal", command=retour_au_menu_principal)
    Retour_Menu_Principal.grid(row=1, column=1)


#Fonction qui sert à exporter les résultats vers Excel
def export_to_csv(result):
    with open('customers.csv', 'a', newline="") as f:
        w = csv.writer(f, dialect='excel')
        for record in result:
            w.writerow(record)
    

#Interface pour afficher tous les èlus
def afficher_elus_interface():
    global root
    root.destroy()
    root = Tk()
    root.title('Formation Continue')
    root.geometry("1150x500")
    Id_Label = Label(root, text="Numéro (Id)", font=("Helvetica, 14"))
    Id_Label.grid(row=0, column=0)
    Nom_Label = Label(root, text="Nom", font=("Helvetica, 14"))
    Nom_Label.grid(row=0, column=1)
    Prenom_Label = Label(root, text="Prenom", font=("Helvetica, 14"))
    Prenom_Label.grid(row=0, column=2)
    Telephone_Label = Label(root, text="Telephone", font=("Helvetica, 14"))
    Telephone_Label.grid(row=0, column=3)
    Email_Label = Label(root, text="Email", font=("Helvetica, 14"))
    Email_Label.grid(row=0, column=4)
    Niveau_Etudes_Label = Label(root, text="Niveau d'études", font=("Helvetica, 14"))
    Niveau_Etudes_Label.grid(row=0, column=5)
    Fonction_Label = Label(root, text="Fonction", font=("Helvetica, 14"))
    Fonction_Label.grid(row=0, column=6)
    Souhait_Label = Label(root, text="Souhait", font=("Helvetica, 14"))
    Souhait_Label.grid(row=0, column=7)
    conn = None
    try: 
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("Select elu_id, elu_nom, elu_prenom, elu_telephone, elu_email, elu_niveau_etudes, elu_fonction, elu_souhait from elu")
        result=cur.fetchall()
        for index, i in enumerate(result):
            num = 0
            index += 1
            for y in i:
                elu_label = Label(root, text=y)
                elu_label.grid(row=index, column=num, pady=15, padx=5)
                num += 1
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    csv_button = Button(root, text="Exporter les résultats vers Excel", command=lambda: export_to_csv(result))
    csv_button.place(x=900, y=20)

    Retour_Menu_Principal = Button(root, text="Retourner au Menu Principal", command=retour_au_menu_principal)
    Retour_Menu_Principal.place(x=900, y=60) 
    


afficher_menu_principal()