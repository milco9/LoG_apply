import cv2 as cv
import numpy 

cestaTominko ="D:\Tomas\ING\Pocitacove_videnie_spracovanie_obrazu\proj\zad2\\test_LOG.jpg"

image = cv.imread(cestaTominko)

imageGrey = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

def con(inputImage,inputFilter):
    imageHeight = inputImage.shape[0]
    imageWidth = inputImage.shape[1]
    filterShapeZero = inputFilter.shape[0]
    Kernel = int(numpy.floor(filterShapeZero/2))
    filterHigh=inputFilter.shape[0]
    outputImage=numpy.zeros((imageHeight-filterHigh+1, imageWidth-filterHigh+1))

    for i in range(Kernel,imageHeight-Kernel-1):
        for j in range(Kernel,imageWidth-Kernel-1):
            newSectionInImage=inputImage[i-Kernel:i+1+Kernel,j-Kernel:j+1+Kernel]
            outputImage[i-Kernel,j-Kernel]=numpy.sum(numpy.matmul(newSectionInImage,inputFilter))
    return outputImage

size =3
sigma =0.9
sigmaOn2 =sigma**2
pi=numpy.pi

v = numpy.array(range(-int(numpy.floor(size/2)), int(numpy.ceil(size/2))))

maskMatrix = numpy.ones((size,1))*v
maskMatrixT = maskMatrix.T

maskMatrixOn2=maskMatrix**2
maskMatrixTOn2=maskMatrixT**2

print(maskMatrix)
print(maskMatrixT)



## Gaussian
arg = -(maskMatrixOn2 + maskMatrixTOn2)/(2*sigmaOn2)

h=numpy.exp(arg)


newImage = con(imageGrey,h)
gaussImage = newImage/numpy.max(newImage)

## laplacian

h1=h*(maskMatrixOn2 +maskMatrixTOn2-2*sigmaOn2)/(2*pi*sigma**6)
laplacian=h1-numpy.sum(h1)/(size**2)

laplacian = con(gaussImage,laplacian)
laplacian= laplacian/numpy.max(laplacian)


cv.imshow("LoG",laplacian)



G0=cv.GaussianBlur(imageGrey,(size,size),sigma)
L0 = cv.Laplacian(G0, ddepth=cv.CV_16S, ksize=size)
L0=L0/numpy.max(L0)
cv.imshow("Ukazkove",L0)
cv.waitKey(0)
