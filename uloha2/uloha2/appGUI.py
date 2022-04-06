import tkinter

from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import imageProcessing
import os

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x530")
        self.title(" Uloha2")
        self.path=FALSE
        self.createWigets()
        


    def buttonTrackingClicked(self):
        self.path=True



    def createWigets(self):
        shift = 35
        style = ttk.Style()

        self.buttonDeleteTrackers = ttk.Button(self, text = "Load image", command = self.buttonTrackingClicked)
        self.buttonDeleteTrackers.place(x=680,y=21)

        self.picture = tkinter.Label(self)
        self.picture.place(x=20, y=20)

        style.configure(".", font=(None, 15))


       


