import tkinter

from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("850x530")
        self.title(" Uloha2")
        self.path=FALSE
        self.createWigets()
        self.loadTESTimageFlag = FALSE
        self.imageIsprocesed=FALSE
        self.LoadedTestImage=FALSE
        


    def buttonTrackingClicked(self):
        self.path=True

    def buttonLoadTestImage(self):
        self.loadTESTimageFlag=True

    def buttonLoadedTestImage(self):
        self.LoadedTestImage=True



    def createWigets(self):
        shift = 35
        style = ttk.Style()

        self.buttonLoadImage = ttk.Button(self, text = "Load image", command = self.buttonTrackingClicked)
        self.buttonLoadImage.place(x=680,y=21)

        self.buttonLoadImage = ttk.Button(self, text = "TEST image", command = self.buttonLoadTestImage)
        self.buttonLoadImage.place(x=680,y=81)

        
        self.buttonLoadImage = ttk.Button(self, text = "Loaded image", command = self.buttonLoadedTestImage)
        self.buttonLoadImage.place(x=680,y=141)

        self.picture = tkinter.Label(self)
        self.picture.place(x=20, y=20)

        style.configure(".", font=(None, 15))


       


