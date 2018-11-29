from tkinter import *
from tkinter import messagebox
import sqlite3

class Main:
    def __init__(self, master):
        self.frame = Frame(master, width=1000, height=576)
        self.frame.pack()
        lblWord = Label(self.frame,text="Type the new word!!").pack()
        self.palavra=Entry(self.frame, width=75)
        self.palavra.pack()
        self.separador = Frame(height=2,bd=3,relief=SUNKEN,width=100)
        self.separador.pack(fill=X,pady=5,padx=5)
        self.frame3=Frame(master,width=768, height=576)
        self.frame3.pack()
        self.add = Button(self.frame3,text="Add Word",command=self.adcionar)
        self.add.pack(side=LEFT)
        self.apg = Button(self.frame3,text="Delete Word",command=self.apagar)
        self.apg.pack(side=LEFT)
        scrollbar=Scrollbar(master)
        scrollbar.pack(fill=Y,side=RIGHT)
        self.listbox=Listbox(master,width=100,height=75)
        self.listbox.pack(padx=5,pady=5)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.conectar = sqlite3.connect("words.db")
        self.cursor = self.conectar.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS VOCABULARY(name TEXTO PRIMARY KEY)")
        self.conectar.commit()
        lista = self.cursor.execute("SELECT * FROM VOCABULARY ORDER BY 1 ASC ")

        cont = 0
        for i in lista:
            cont = cont+1
            self.listbox.insert(END, i)

        contWord = (10000 - cont)
        wordcont = ("Words To Complete Vocabulary:: %d" % contWord)
        lblCount = Label(text=wordcont)
        lblCount.place(x=170,y=55)

    def adcionar(self):
        try:
            palavrax = self.palavra.get()
            palavrax = palavrax.upper()
            if palavrax == "":
                messagebox.showwarning(title="Error",message="Insert the word",)
            else:
                self.cursor.execute("insert into VOCABULARY values(?)",(palavrax,  ))
                self.conectar.commit()
                self.listbox.insert(END,palavrax)
                self.listbox.delete(0, END)
                self.palavra.delete(0,END)
                lista = self.cursor.execute("SELECT * FROM VOCABULARY ORDER BY 1 ASC ")
                cont = 0
                for i in lista:
                    cont = cont + 1
                    self.listbox.insert(END, i)
                contWord = (10000 - cont)
                wordcont = ("Words To Complete Vocabulary:: %d" % contWord)
                lblCount = Label(text=wordcont)
                lblCount.place(x=170,y=55)
        except:
            messagebox.showwarning(title="Error", message="The Word '%s' Already exist" %palavrax)

    def apagar(self):
        try:
            palavray = self.palavra.get()
            palavray = palavray.upper()
            if palavray == "":
                messagebox.showwarning(title="Error", message="Insert the word for delete", )
            else:
                self.cursor.execute("DELETE FROM VOCABULARY where name=(?)", (palavray,))
                self.conectar.commit()
                self.listbox.delete(0, END)
                lista = self.cursor.execute("SELECT * FROM VOCABULARY ORDER BY 1 ASC ")
                cont = 0
                for i in lista:
                    cont = cont + 1
                    self.listbox.insert(END, i)
                messagebox.showwarning(title="Word Deleted", message="The word '%s' was successfully deleted" %palavray)
                contWord = (10000 - cont)
                wordcont = ("Words To Complete Vocabulary:: %d" % contWord)
                lblCount = Label(text=wordcont)
                lblCount.place(x=170,y=55)
        except:
            messagebox.showwarning(title="Error", message="Something is wrong to delete. Please check and try again.")
def fechar():
    if messagebox.askyesno(title="Close App",message="Do you really wish close the application? "):
        exit()
    else:
        pass
root=Tk()
root.geometry("940x450")
root.title("My Vocabulary")
root.protocol("WM_DELETE_WINDOW",fechar)

Main(root)
root.mainloop()

