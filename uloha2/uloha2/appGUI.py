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
        self.loadDEFAULTimageFlag = FALSE
        self.imageIsprocesed=FALSE
        self.LoadedTestImage=FALSE
        self.textLabel="Just do it"
        self.loadGaussImageFlag=FALSE
        self.loadLaplacianimageFlag=FALSE
        


    def buttonSetPathToImage(self):
        self.path=True

    def buttonDefLoadImage(self):
        self.loadDEFAULTimageFlag=True

    def buttonLaplacianImage(self):
        self.loadLaplacianimageFlag=True

    def buttonGaussImage(self):
        self.loadGaussImageFlag=True

    def buttonLoadedTestImage(self):
        self.LoadedTestImage=True



    def createWigets(self):
        shift = 35
        style = ttk.Style()

        self.buttonLoadImage = ttk.Button(self, text = "Load image", command = self.buttonSetPathToImage)
        self.buttonLoadImage.place(x=680,y=21)

        self.buttonDefaultImage = ttk.Button(self, text = "TEST image", command = self.buttonDefLoadImage)
        self.buttonDefaultImage.place(x=680,y=81)


        self.labelText = Label(self, text="INFO", font=("Helvetica", 16))
        self.labelText.place(x=680,y=141)

        lText = Label(self, text="Show image :", font=("Helvetica", 12))
        lText.place(x=680,y=201)

        self.buttonshowGauss = ttk.Button(self, text = "Gauss image", command = self.buttonGaussImage)
        self.buttonshowGauss.place(x=680,y=231)

        self.buttonshowLaplacian = ttk.Button(self, text = "Lapla. image", command = self.buttonLaplacianImage)
        self.buttonshowLaplacian.place(x=680,y=291)

        self.buttonShowLoadedImage = ttk.Button(self, text = "Loaded image", command = self.buttonLoadedTestImage)
        self.buttonShowLoadedImage.place(x=680,y=351)

        self.picture = tkinter.Label(self)
        self.picture.place(x=20, y=20)

        style.configure(".", font=(None, 15))
    
    def updateText(self,inputText):
        self.labelText.configure(text=inputText)


       


