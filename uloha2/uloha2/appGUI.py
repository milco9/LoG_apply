import tkinter
import cv2

from tkinter import *
from tkinter import ttk, filedialog,messagebox
from tkinter.filedialog import askopenfile


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        #self.geometry("100x530")
        self.title(" Uloha2")
        self.path=FALSE
        self.loadDEFAULTimageFlag = FALSE
        self.imageIsprocesed=FALSE
        self.LoadedTestImage=FALSE
        self.loadGaussImageFlag=FALSE
        self.loadLaplacianimageFlag=FALSE
        self.closeFlag=FALSE
        self.pictureHight=10
        self.pictureWidth=10
        self.logImageFlag=False
        self.createWigets()
        


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
    
    def buttonLOGImage(self):
        self.logImageFlag=True



    def createWigets(self):
        style = ttk.Style()

        xShiftPicture =0
        xShiftWidgets=30+xShiftPicture
        self.xGeometry = xShiftWidgets+150+self.pictureWidth
        print(self.xGeometry)
        self.yGeometry = 580

        self.buttonLoadImage = ttk.Button(self, text = "Load image", command = self.buttonSetPathToImage)
        self.buttonLoadImage.place(x=xShiftWidgets,y=21)

        self.buttonDefaultImage = ttk.Button(self, text = "TEST image", command = self.buttonDefLoadImage)
        self.buttonDefaultImage.place(x=xShiftWidgets,y=81)


        self.labelText = Label(self, text="INFO", font=("Helvetica", 16))
        self.labelText.place(x=xShiftWidgets,y=141)

        lText = Label(self, text="Show image :", font=("Helvetica", 12))
        lText.place(x=xShiftWidgets,y=201)

        self.buttonshowGauss = ttk.Button(self, text = "Gauss image", command = self.buttonGaussImage)
        self.buttonshowGauss.place(x=xShiftWidgets,y=231)

        self.buttonshowLaplacian = ttk.Button(self, text = "Lapla. image", command = self.buttonLaplacianImage)
        self.buttonshowLaplacian.place(x=xShiftWidgets,y=291)

        self.buttonShowLoadedImage = ttk.Button(self, text = "Loaded image", command = self.buttonLoadedTestImage)
        self.buttonShowLoadedImage.place(x=xShiftWidgets,y=351)

        self.buttonLoGImage = ttk.Button(self, text = "Orig Log fcn", command = self.buttonLOGImage)
        self.buttonLoGImage.place(x=xShiftWidgets,y=411)

        self.closeButton = ttk.Button(self, text = "Close program", command = self.closeFunction)
        self.closeButton.place(x=xShiftWidgets,y=481)

        self.picture = tkinter.Label(self)
        self.picture.place(x=20, y=20)


        style.configure(".", font=(None, 15))

        alignstr = '%dx%d' % (self.xGeometry, self.yGeometry)
        self.geometry(alignstr)

        resizableFag=True
        self.resizable(width=resizableFag, height=resizableFag)

    
    def updateText(self,inputText):
        self.labelText.configure(text=inputText)

    def closeFunction(self):
        self.closeFlag=TRUE



       


