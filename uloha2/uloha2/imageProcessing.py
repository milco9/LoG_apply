from pickle import FALSE, TRUE
from sys import flags
import cv2
import numpy
import PIL.ImageTk
import PIL.Image
from cv2 import rectangle
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import appGUI

from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os




class ImgProc():


    def __init__(self,app):
        self.tracking = False
        self.fps = 0
        self.filepath =" "
        self.filepathExist=False


    def buttonSetPathClicked(self):

        file = filedialog.askopenfile(mode='r', filetypes=[("Image Files", ".png .jfif, .jpg, .jpeg")])
        if file:
            self.filepath = os.path.abspath(file.name)
            self.filepathExist =TRUE
     
            

    def con(self,inputImage,inputFilter):
        imageHeight = inputImage.shape[0]
        imageWidth = inputImage.shape[1]
        filterShapeZero = inputFilter.shape[0]
        K = int(numpy.floor(filterShapeZero/2))
        filterHigh=inputFilter.shape[0]
        outputImage=numpy.zeros((imageHeight-filterHigh+1, imageWidth-filterHigh+1))

        for i in range(K,imageHeight-K-1):
            for j in range(K,imageWidth-K-1):
                newSectionInImage=inputImage[i-K:i+1+K,j-K:j+1+K]
                outputImage[i-K,j-K]=numpy.sum(numpy.matmul(newSectionInImage,inputFilter))
        return outputImage

    def functionLoG(self,img,size,sigma):

            G0=cv2.GaussianBlur(img,(size,size),sigma)
            L0 = cv2.Laplacian(G0, ddepth=cv2.CV_16S, ksize=size)
            L0=L0/numpy.max(L0)
            cv2.imshow("Ukazkove",L0)
            cv2.waitKey(0)

    def preprocessIMG(self,img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return img

    def GAUSS(self,img,maskMatrixOn2,maskMatrixTOn2,sigmaOn2):
            arg = -(maskMatrixOn2 + maskMatrixTOn2)/(2*sigmaOn2)

            h=numpy.exp(arg)

            newImage = self.con(img,h)
            gImage = newImage/numpy.max(newImage)
            return gImage,h

    def LAPLACIAN(self,img,h,size):

            laplacian=h-numpy.sum(h)/(size**2)

            laplacian = self.con(img,laplacian)
            laplacian= laplacian/numpy.max(laplacian)

            return laplacian
            

    def imgConvert(self):
        GUI = appGUI.App()


        print(str(self.filepath))
        if self.filepathExist is TRUE:
            
            self.filepathExist = False
            GUI.path=False

            size =3
            sigma =0.9
            sigmaOn2 =sigma**2
            pi=numpy.pi


            image = cv2.imread(self.filepath)

            img=self.preprocessIMG(image)



            v = numpy.array(range(-int(numpy.floor(size/2)), int(numpy.ceil(size/2))))

            maskMatrix = numpy.ones((size,1))*v
            maskMatrixT = maskMatrix.T

            maskMatrixOn2=maskMatrix**2
            maskMatrixTOn2=maskMatrixT**2

            ## Gaussian

            gImage,h=self.GAUSS(img,maskMatrixOn2,maskMatrixTOn2,sigmaOn2)

            ## laplacian
            h=h*(maskMatrixOn2 +maskMatrixTOn2-2*sigmaOn2)/(2*pi*sigma**6)
            lImage=self.LAPLACIAN(gImage,h,size)
            
            

            
            cv2.imshow("LoG",lImage)

            #self.functionLoG(imageGrey,size,sigma)

            self.convertImage(lImage)

            return self.imgtk
        
    def convertImage(self, cv2image):
        img = PIL.Image.fromarray(cv2image)
        self.imgtk = PIL.ImageTk.PhotoImage(image=img)
