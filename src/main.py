# coding: utf-8
 
import tkinter as tk
import tkinter.ttk as TTK
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import os
import shutil
import database
import pupil
import polar
import binarization

kp=[]

def compare():
   if kp==[]:
      try:
         if filepath:
            analyse()
            database.compare(desc)
      except NameError:
         showwarning('erreur', 'Veuillez selectionner une image')
   else:
      database.compare(desc)
   

def send_data():
   nom = E1.get()
   prenom = E2.get()
   database.add(nom,prenom,kp,desc)
   window.destroy()

def input_win():
   global E1
   global E2
   global window
   print(desc.size)
   window = tk.Toplevel(fenetre)
   window.title("Iris Authentification - Ajout valeur")
   window.resizable(width=False, height=False)
   window.iconbitmap('../icon/favicon.ico')
   Label(window, text="Nom: ").grid(row=1,column=0)
   E1 = Entry(window, bd =5)
   E1.grid(row=1,column=1)
   Label(window, text="Prénom: ").grid(row=2,column=0)
   E2 = Entry(window, bd =5)
   E2.grid(row=2,column=1)
   Button(window, text ='Ajouter',relief=GROOVE,height = 3, width = 10,command=send_data).grid(row=3,column=1)
   

def ajouter_features():
   if kp==[]:
      try:
         if filepath:
            analyse()
            input_win()
         
      except NameError:
         showwarning('erreur', 'Veuillez selectionner une image')
   else:
      input_win()
      
def remove_db():
   os.remove('../eye_database.db')

def delete_temp():
   shutil.rmtree('temp')
    
def show_result():
    img_final = Image.open('temp/final.png')
    img_final = img_final.resize((int(width_W/4),int(height_W/3)),Image.ANTIALIAS)
    img_final = ImageTk.PhotoImage(img_final)
    label_final.configure(image=img_final)
    label_final.image = img_final

    img_border = Image.open('temp/p.png')
    img_border = img_border.resize((int(width_W/4),int(height_W/3)),Image.ANTIALIAS)
    img_border = ImageTk.PhotoImage(img_border)
    label_border.configure(image=img_border)
    label_border.image = img_border
    

    img_center = Image.open('temp/m.png')
    img_center = img_center.resize((int(width_W/4),int(height_W/3)),Image.ANTIALIAS)
    img_center = ImageTk.PhotoImage(img_center)
    label_center.configure(image=img_center)
    label_center.image = img_center

    img_polar = Image.open('temp/polar.png')
    img_polar = img_polar.resize((int(width_W/1.5),int(height_W/2)),Image.ANTIALIAS)
    img_polar = ImageTk.PhotoImage(img_polar)
    label_polar.configure(image=img_polar)
    label_polar.image = img_polar
    
    
    
    
def import_image():
    global image
    global filepath
    default_analyse.config(text='Non effectué',fg='red')
    default_analyse.configure()
    filepath = askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('all files','.*')])
    canvas_image.delete(txt)
    image = Image.open(filepath)
    image= ImageTk.PhotoImage(image)
    canvas_image.itemconfig(im,image =image)
    canvas_image.configure()


def verif_db():
     if askyesno('Suppression DB', 'Êtes-vous sûr de vouloir faire ça?'):
        remove_db()
        showwarning('confirmation suppression', 'La DB a été supprimé!')


def analyse():
    if not os.path.exists('temp'):
       os.makedirs('temp')
    center = pupil.isolate_pupil(filepath)
    polar.polar2linear(center)
    global kp
    global desc
    kp,desc = binarization.features()
    default_analyse.config(text='Analyse effectuée!',fg='green')
    default_analyse.configure()
    show_result()
    delete_temp()
    

 
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

fenetre = Tk()
width_W = int(width/2)
height_W = int(height/2)+150
fenetre.geometry(str(width_W)+'x'+str(height_W)+'+'+str(int(width/4))+'+'+str(int(height/4)-150))
fenetre.title("Iris Authentification")
fenetre.resizable(width=False, height=False)
fenetre.iconbitmap('../icon/favicon.ico')


menubar = Menu(fenetre)
menu_file= Menu(menubar, tearoff=0)
menu_file.add_command(label="Importer", command=import_image)
menu_file.add_separator()
menu_file.add_command(label="Quitter", command=fenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menu_file)


menu_db= Menu(menubar, tearoff=0)
menu_db.add_command(label="Ajouter", command=ajouter_features)
menu_db.add_command(label="Supprimer", command=verif_db)
menu_db.add_separator()
menu_db.add_command(label="Quitter", command=fenetre.destroy)
menubar.add_cascade(label="Database", menu=menu_db)
fenetre.config(menu=menubar)


canvas_image = Canvas(fenetre,width=230, height=230)
im = canvas_image.create_image(125,125, image='')
txt = canvas_image.create_text(115,115, text="no image", font="Arial 16 italic", fill="red")
canvas_image.place(relx=0.5, rely=0.18, anchor=CENTER)

Button(fenetre, text ='Analyser',relief=GROOVE,height = 5, width = 33,command=analyse).place(relx=0.20, rely=0.10, anchor=CENTER)
Button(fenetre, text ='Comparer',relief=GROOVE,height = 5, width = 33,command=compare).place(relx=0.20, rely=0.27, anchor=CENTER)

Label(fenetre, text="Etat Analyse: ").place(relx=0.72, rely=0.10, anchor=CENTER)
default_analyse= Label(fenetre, text="Non effectué",fg="red")
default_analyse.place(relx=0.82, rely=0.10, anchor=CENTER)

n = TTK.Notebook(fenetre,width=width_W,height=(int(height_W/2)))
onglet1 = TTK.Frame(n)
onglet2 = TTK.Frame(n)
n.add(onglet1, text='Segmentation')
n.add(onglet2,text='Polarisation')
n.place(relx=0.50,rely=0.80,anchor=CENTER)

label_center = Label(onglet1,image='')
label_center.place(relx=0.20,rely=0.40,anchor=CENTER)

label_border = Label(onglet1,image='')
label_border.place(relx=0.50,rely=0.40,anchor=CENTER)

label_final = Label(onglet1,image='')
label_final.place(relx=0.80,rely=0.40,anchor=CENTER)

label_polar = Label(onglet2,image='')
label_polar.place(relx=0.50,rely=0.40,anchor=CENTER)

database.init_database()

fenetre.mainloop()
