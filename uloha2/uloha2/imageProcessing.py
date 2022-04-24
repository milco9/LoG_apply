from pickle import FALSE, TRUE
import cv2
import numpy
import PIL.ImageTk
import appGUI
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


    def loadTESTimage(self):
        file = os.getcwd()
        file=file+"\\test_LOG.jpg" 
        if file:
            self.filepath = file
            self.filepathExist =TRUE

    def buttonSetPathClicked(self):

        file = filedialog.askopenfile(mode='r', filetypes=[("Image Files", ".png .jfif, .jpg, .jpeg")])
        if file:
            self.filepath = os.path.abspath(file.name)
            self.filepathExist =TRUE
         
    def conLap(self,inputImage,inputFilter):

        ## Zistujeme informacie o oprazku a o filtry pre forka
        imageHeight = inputImage.shape[0]
        imageWidth = inputImage.shape[1]
        filterShapeZero = inputFilter.shape[0]
        K = int(numpy.floor(filterShapeZero/2))
        filterHigh=inputFilter.shape[0]
        filterWidth=inputFilter.shape[1]

        newImageHeight=imageHeight-filterHigh+1
        newImageWidth =imageWidth-filterWidth+1
        ## Vytvorime prazdny image
        outputImage=numpy.zeros((newImageHeight, newImageWidth))
        ## Aplikovanie konvolucie
        for i in range(K,imageHeight-K-1):
            for j in range(K,imageWidth-K-1):
                newSectionInImage=inputImage[i-K:i+1+K,j-K:j+1+K]
                imageXfilter=numpy.matmul(newSectionInImage,inputFilter)
                outputImage[i-K,j-K]=numpy.sum(imageXfilter)
        outputImage= outputImage/numpy.max(outputImage)
        
        return outputImage

    def pythonFunctionLoG(self,img,size,sigma):

            G0=cv2.GaussianBlur(img,(size,size),sigma)
            L0 = cv2.Laplacian(G0, ddepth=cv2.CV_16S, ksize=size)
            L0=L0/numpy.max(L0)
            cv2.imshow("Ukazkove",L0)
            cv2.waitKey(0)

    def preprocessIMG(self,img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return img

    def createFilter(self,maskMatrixOn2,maskMatrixTOn2):
        _,size,sigma =self.variables()

        pi=numpy.pi
        sigmaOn2=sigma**2

        h=(numpy.exp(-(maskMatrixOn2 + maskMatrixTOn2)/(2*sigmaOn2)))

        h=h*(maskMatrixOn2 +maskMatrixTOn2-2*sigmaOn2)/(2*pi*sigma**6)

        laplacianFilter=h-numpy.sum(h)/(size**2)

        return laplacianFilter

    def LAPLACIAN(self,img,maskMatrixOn2,maskMatrixTOn2):

                ## taktiez najskor si vytvorime filter
            laplacianFilter=self.createFilter(maskMatrixOn2,maskMatrixTOn2)

            if self.firstLap is TRUE:
                print(laplacianFilter)
                self.firstLap=FALSE

            laplacian = self.conLap(img,laplacianFilter)

            

            return laplacian

    def GAUSS(self,img):

        B,G,R = cv2.split(img)
        img_GB = self.applyFilter(B)
        img_GG = self.applyFilter(G)
        img_GR = self.applyFilter(R)
        img = cv2.merge([img_GB,img_GG,img_GR])
        self.gImage=img
        img=self.preprocessIMG(img)

        return img

    def createKernelGauss(self):

        k,size,sigma =self.variables()

        pi=numpy.pi
        ker = numpy.zeros((size,size),numpy.float32)
        for i in range (size):
            for j in range (size):
                n = -((i-k)**2 + (j-k)**2)
                ker[i,j] = m.exp(n/(2*(sigma**2)))/2*pi*(sigma**2)
        ker= ker/(numpy.sum(ker)) 
        return ker

    def applyFilter(self,img_gray):

            ## Naciatanie premennych o filtri
        k,_,_ =self.variables()

            ## Vytvorenie filtra
        kernel = self.createKernelGauss()

        if self.firstGauss is TRUE:
            print(kernel)
            self.firstGauss=FALSE

        height,width = img_gray.shape
        kernel_height,_ = kernel.shape
        
        halfKernelHeight = (int(kernel_height/2))

        rowRange =(halfKernelHeight,height-halfKernelHeight)
        colRange =(halfKernelHeight,width-halfKernelHeight)

                ## Aplikovanie filtra na obrazok kde sa spravy konvolucia tj vynasobi sa filter kazdym pixelom a nahradi sa suma v obrazku na danych indexoch
        for i in range(rowRange[1]):
            for j in range(colRange[1]):
                sum = 0
                for k in range(0,kernel_height):
                    for r in range(0,kernel_height):
                        sum += img_gray[i-halfKernelHeight+k,j-halfKernelHeight+r]*kernel[k,r]
                img_gray[i,j] = sum
        return img_gray

    def variables(self):  
        k=1
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
            
            # Vytvori sa pole -1 0 1
            v = numpy.array(range(-int(numpy.floor(size/2)), int(numpy.ceil(size/2)))) 

            # Z pola sa vytvori matica
            maskMatrix = numpy.ones((size,1))*v
            maskMatrixT = maskMatrix.T

            maskMatrixOn2=maskMatrix**2
            maskMatrixTOn2=maskMatrixT**2

            ## Gaussian 
            print("gauss")

            gImage_grey=self.GAUSS(self.loadedImage)


            ## laplacian
            print("lap")
            lImage=self.LAPLACIAN(gImage_grey,maskMatrixOn2,maskMatrixTOn2)

            
            print("end")
            

            cv2.imshow("LoG",lImage)

            self.imageIsprocesedFlag=TRUE

            

            self.convertImage(lImage)

            print(lImage.shape)
            h,w=lImage.shape

            
            return h,w,self.imgtk
            
    def showLoadedImage(self):
        cv2.imshow("Loaded Image",self.loadedImage)

    def showGaussImageImage(self):
        cv2.imshow("Gauss",self.gImage)

    def showLaplacianOriginalImage(self):

        _,size,sigma =self.variables()
          
        v = numpy.array(range(-int(numpy.floor(size/2)), int(numpy.ceil(size/2))))
        
        maskMatrix = numpy.ones((size,1))*v
        maskMatrixT = maskMatrix.T

        maskMatrixOn2=maskMatrix**2
        maskMatrixTOn2=maskMatrixT**2

        image_grey=self.preprocessIMG(self.loadedImage)
        self.lImageOrig=self.LAPLACIAN(image_grey,maskMatrixOn2,maskMatrixTOn2)
        cv2.imshow("Laplacian",self.lImageOrig)
    
    def getFalgImageisProcesed(self):
        return self.imageIsprocesedFlag

    def getLOGpythonfunctions(self):
        _,size,sigma =self.variables()
        self.pythonFunctionLoG(self.loadedImage,size,sigma)

    def convertImage(self, image):
        img = PIL.Image.fromarray(image)
        self.imgtk = PIL.ImageTk.PhotoImage(image=img)
        


        





