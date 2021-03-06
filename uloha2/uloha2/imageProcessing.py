from pickle import FALSE, TRUE
import cv2
import numpy
import PIL.ImageTk
import appGUI
import matplotlib.pyplot
import math as m
from tkinter import filedialog
import os


class ImgProc():


    def __init__(self,app):
        self.tracking = False
        self.fps = 0
        self.filepath =" "
        self.filepathExist=False
        self.loadedImage= []
        self.gImage=[]
        self.lImageOrig=[]
        self.imageIsprocesedFlag=False
        self.firstGauss=TRUE
        self.firstLap=TRUE
        self.k=1     ## Odskusane velkosti filtra kde k=1;2;4
        self.GaussFilter=[]
        self.LoGFilter=[]
        self.lImage = []


    def loadTESTimage(self):
        file = os.getcwd()
        file=file+"\\test_LOG.jpg" 
        if file:
            self.filepath = file
            self.filepathExist =TRUE

    def buttonSetPathClicked(self):

        file = filedialog.askopenfile(mode='r', filetypes=[("Image Files", ".png .jfif, .jpg, .jpeg, .JPG")])
        if file:
            self.filepath = os.path.abspath(file.name)
            self.filepathExist =TRUE
         
    def con(self,inputImage,mask):

        ## Zistujeme informacie o oprazku a o filtry pre forka
        imageHeight = inputImage.shape[0]
        imageWidth = inputImage.shape[1]
        filterShapeZero = mask.shape[0]
        K = int(numpy.floor(filterShapeZero/2))
        filterHigh=mask.shape[0]
        filterWidth=mask.shape[1]

        newImageHeight=imageHeight-filterHigh+1
        newImageWidth =imageWidth-filterWidth+1

        ## Vytvorime prazdny image
        outputImage=numpy.zeros((newImageHeight, newImageWidth))

        irange=imageHeight-K-1
        jrange=imageWidth-K-1

        ## Aplikovanie konvolucie
        ## Prechadzame obrazok pricom sa vzdy vytiahne z obrazka taka ista velkost aky je velky filter a tieto dve casti tj vytiahnuta cast z obrazka vo forme matice a maska a posielaju sa do funkcie matrixMultiply.
        for i in range(K,irange):
            imageIrange=i+1+K
            for j in range(K,jrange):
                imageJrange=j+1+K
                outputImage[i-K,j-K]=self.matrixMultiply(inputImage[i-K:imageIrange,j-K:imageJrange],mask)

        outputImage= outputImage/numpy.max(outputImage)
        
        return outputImage

    def matrixMultiply(self,imageMatrix,filterMatrix):
        
        img_height,img_width = imageMatrix.shape

        outputSUM=0
        outputMatrix=numpy.zeros((img_height, img_width))

        ## nasledne v tejtu funkcii aplikujeme masku/filter na vytiahnutu maticu z obrazka pomocou dvoch forov kde sa vlastne nasoba jednotlive elementy oboch matic 
        ## a v celkovej sume posielaju naspat do obrazka 
        for i in range (len(imageMatrix)):
            for j in range (len(filterMatrix)):
                    outputMatrix[i][j]= imageMatrix[i][j]*filterMatrix[i][j]
                    outputSUM +=outputMatrix[i][j]
        
        return outputSUM

    def pythonFunctionLoG(self,img,size,sigma):
            ## tato funkcia nam len preukauje pouzitie ukazkovych funkcii dany obrazok sa nikde neposiela iba sa rovno vykresli do okna "Ukazkove"
            G0=cv2.GaussianBlur(img,(size,size),sigma)
            L0 = cv2.Laplacian(G0, ddepth=cv2.CV_16S, ksize=size)
            L0=L0/numpy.max(L0)
            cv2.imshow("Ukazkove",L0)

    def preprocessIMG(self,img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return img

    def createFilter(self):
            ## v tejto funkcii vytvorime LoG masku
        _,size,sigma =self.variables()

        # Vytvori sa vektor -1 0 1
        minusRange = -int(numpy.floor(size/2))
        plusRange =int(numpy.ceil(size/2))
        vector = numpy.array(range(minusRange,plusRange))

        # Z vektora sa vytvori matica
        maskMatrix = numpy.ones((size,1))*vector
        maskMatrixT = maskMatrix.T

        maskMatrixOn2=maskMatrix**2
        maskMatrixTOn2=maskMatrixT**2

        pi=numpy.pi
        sigmaOn2=sigma**2

        ## exponent
        exp=(numpy.exp(-(maskMatrixOn2 + maskMatrixTOn2)/(2*sigmaOn2)))

        maskLap=-(1/(pi*sigma**4))*(1-(maskMatrixOn2 + maskMatrixTOn2)/(2*sigmaOn2))*exp

        ## pouzity vzorec https://homepages.inf.ed.ac.uk/rbf/HIPR2/log.htm

        laplacianFilter=maskLap-numpy.sum(maskLap)/(size**2)
        self.LoGFilter=laplacianFilter

        return laplacianFilter

    def LAPLACIAN(self,img):

            ## taktiez najskor si vytvorime filter/maska
            laplacianFilter=self.createFilter()

            if self.firstLap is TRUE:
                print(laplacianFilter)
                self.firstLap=FALSE
            ## aplikovanie konvolucie 
            laplacian = self.con(img,laplacianFilter)

            

            return laplacian

    def GAUSS(self,img):

        ## vytvorenie masku
        mask = self.createMaskForGauss()
        if self.firstGauss is TRUE:
            print(mask)
            self.firstGauss=FALSE

        img=self.preprocessIMG(img)
        ## aplikovanie konvolucie na obrazok 
        img = self.con(img,mask)
         

        ## Zapisanie do globalnej premennej na zobrazenie gauusiana
        self.gImage=img
        
        return img

    def createMaskForGauss(self):
            ## v tejto zase vytvorima masku gauss filtra
        k,size,sigma =self.variables()

        sigmaOn2=sigma**2

        pi=numpy.pi
        mask = numpy.zeros((size,size),numpy.float32)
        for i in range (size):
            for j in range (size):
                ikOn2=(i-k)**2
                jkOn2=(j-k)**2
                n = -(ikOn2 + jkOn2)
                mask[i,j] = m.exp(n/(2*sigmaOn2))/2*pi*sigmaOn2

        mask= mask/(numpy.sum(mask)) 

        self.GaussFilter=mask

        return mask                

    def variables(self):  
        k=self.k
        size = 2*k+1
        sigma =0.9     

        return k,size,sigma  

    def imgConvert(self):

        
        print(str(self.filepath))

        if self.filepathExist is TRUE:
            
            ## tuna sa len nacitaju premenne 
            _,size,sigma =self.variables()

            ## nacita sa zadany obrazok
            self.loadedImage = cv2.imread(self.filepath)
            

            ## Gaussian 
            print("gauss")

            gImage_grey=self.GAUSS(self.loadedImage)

            
            ## laplacian
            print("lap")
            self.lImage=self.LAPLACIAN(gImage_grey)

                    
            print("end")
            

            cv2.imshow("LoG",self.lImage)

            self.imageIsprocesedFlag=TRUE
            

            self.convertImage(self.lImage)
            
            return self.imgtk

    def zero_cross_detection(self,inImage):

        ZC_img = numpy.zeros(inImage.shape)

        imageHeight = inImage.shape[0]
        imageWidth = inImage.shape[1]

        for i in range(1,imageHeight):
            for j in range(1,imageWidth):
                if inImage[i][j]>0:
                    if inImage[i+1][j] < 0:
                        ZC_img[i,j] = 1
                    elif inImage[i+1][j+1] < 0:
                        ZC_img[i,j] = 1
                    elif inImage[i][j+1] < 0:
                        ZC_img[i,j] = 1
                    elif inImage[i-1][j] < 0:
                        ZC_img[i,j] = 1
                elif inImage[i][j] < 0:
                    if inImage[i+1][j] > 0:
                        ZC_img[i,j] = 0
                    elif inImage[i+1][j+1] > 0:
                        ZC_img[i,j] = 0
                    elif inImage[i][j+1] > 0:
                        ZC_img[i,j] = 0
                    elif inImage[i-1][j] > 0:
                        ZC_img[i,j] = 0

        return ZC_img
            
    def showLoadedImage(self):
        cv2.imshow("Loaded Image",self.loadedImage)

    def showGaussImageImage(self):
        cv2.imshow("Gauss",self.gImage)

    def showZCImage(self):        
        img=self.zero_cross_detection(self.lImage)
        cv2.imshow("Z-C_image",img)
    
    def getFalgImageisProcesed(self):
        return self.imageIsprocesedFlag

    def getLOGpythonfunctions(self):
        _,size,sigma =self.variables()
        self.pythonFunctionLoG(self.loadedImage,size,sigma)

    def convertImage(self, image):
        img = PIL.Image.fromarray(image)
        self.imgtk = PIL.ImageTk.PhotoImage(image=img)

    def showFIlterGraph(self):
        fig, axes = matplotlib.pyplot.subplots(nrows=2, ncols=1, constrained_layout=True, figsize=matplotlib.pyplot.figaspect(1))
        graphGauss = axes[0].pcolormesh(self.GaussFilter)
        fig.colorbar(graphGauss, ax=axes[0])
        graphLoG = axes[1].pcolormesh(self.LoGFilter)
        fig.colorbar(graphLoG, ax=axes[1])
        matplotlib.pyplot.show()
                
        


        





