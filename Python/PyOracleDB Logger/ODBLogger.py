#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter import messagebox, font
import cx_Oracle
import json
from PIL import Image, ImageTk


class Logger:

    def __init__(self):
        self.__read_bases__()
        self.__create_box__()

    def __read_bases__(self):
        with open('bases.json', 'r') as file:
            self.bases = json.load(file)

    def __create_box__(self):
        global userE
        global passE
        global var
        global rootA

        rootA = Tk()
        rootA.title("Oracle Database Logger")

        box_width = 300
        box_height = 200
        screen_width = rootA.winfo_screenwidth()
        screen_height = rootA.winfo_screenheight()
        center_width = int((screen_width / 2) - (box_width / 2))
        center_height = int((screen_height / 2.25) - (box_height / 2))
        rootA.geometry(f"{box_width}x{box_height}+{center_width}+{center_height}")

        userE = StringVar()
        passE = StringVar()
        var = StringVar()
        var.set("Select")

        img = Image.open('logo.png')
        img = ImageTk.PhotoImage(img)
        imglabel = Label(rootA, imag=img)
        imglabel.place(x=35, y=20)

        instruction = Label(rootA, text="Log in to database", font=("arial", 14))
        instruction.place(x=80, y=5)
        f = font.Font(instruction, instruction.cget("font"))
        f.configure(underline=True)
        instruction.configure(font=f)

        nameL = Label(rootA, text="Username: ")
        passL = Label(rootA, text="Password: ")
        baseL = Label(rootA, text="Database: ")
        nameL.place(x=20, y=40)
        passL.place(x=20, y=70)
        baseL.place(x=20, y=100)

        nameEL = Entry(rootA, textvar=userE)
        passEL = Entry(rootA, textvar=passE, show='*')

        baseEL = OptionMenu(rootA, var, *self.bases.keys())
        nameEL.place(x=120, y=40)
        passEL.place(x=120, y=70)
        baseEL.config(width=12)
        baseEL.place(x=120, y=95)

        loginB = Button(rootA, text="Log in", command=self.__get_creds__, height=1, width=8)
        loginB.place(x=30, y=150)

        cancelB = Button(rootA, text="Cancel", command=rootA.destroy, height=1, width=8)
        cancelB.place(x=200, y=150)

        rootA.mainloop()

    def __get_creds__(self):
        if userE.get() == "" or passE.get() == "" or var.get() == "Select":
            pass
        else:
            self.username = userE.get()
            self.password = passE.get()
            self.base = self.bases[var.get()]
            self.__log_in__()
            try:
                rootA.destroy()
            except TclError:
                pass

    def __log_in__(self):
        try:
            self.dsnStr = cx_Oracle.makedsn(self.base['hostname'], self.base['port'], self.base['sid'])
            self.con = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.dsnStr)
            self.cur = self.con.cursor()
            messagebox.showinfo("Logged in", f"Connection with database {self.base['sid']} established")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            messagebox.showerror("DatabaseError", f"Unable to connect to {self.base['sid']} database.\n{error.message}")
            var.set("Select")
            passE.set("")
            userE.set("")
            rootA.mainloop()
        finally:
            try:
                del self.password
            except AttributeError:
                pass

    def get_connection(self):
        return self.con

    def get_cursor(self):
        return self.cur

    def close_connection(self):
        try:
            self.cur.close()
            self.con.close()
        except AttributeError:
            pass


if __name__ == "__main__":
    log = Logger()
    log.close_connection()
