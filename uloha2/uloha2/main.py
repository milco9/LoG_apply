##################### ZadaniePVSO uloha 2 MAIN #####################
# Autor: Michal Molnar & Tomas Nyiri

from cProfile import label
from pickle import FALSE, TRUE
import appGUI
import cv2
import imageProcessing as imgProc


def main():
    GUI = appGUI.App()
    imageProcess = imgProc.ImgProc(GUI)
    pathIsSaved= FALSE
    GUI.updateText("CHOOS img")
    GUI.update()

    imageProcess.k=2 ## Odskusane velkosti filtra kde k=1;2;4


    while True:
        
        if GUI.path:
            imageProcess.buttonSetPathClicked()
            GUI.path=False

        if GUI.loadDEFAULTimageFlag:
            imageProcess.loadTESTimage()
            GUI.loadDEFAULTimageFlag=False

        if imageProcess.filepathExist: 
            GUI.updateText("Image is loaded") 
            GUI.update()
            GUI.pictureHight,GUI.pictureWidth,imageConverted=imageProcess.imgConvert()
            pathIsSaved= TRUE
            imageProcess.filepathExist=False
            GUI.update()
            #GUI.picture.configure(image=imageConverted)
            GUI.imageIsprocesed=imageProcess.getFalgImageisProcesed()


        if GUI.loadLaplacianimageFlag:
            if pathIsSaved: 
                GUI.updateText("LAP show")
                GUI.loadLaplacianimageFlag=FALSE
                GUI.update()
                imageProcess.showLaplacianOriginalImage()
            else:
                GUI.updateText("LOAD PICTUE !")
                GUI.loadLaplacianimageFlag=FALSE
                GUI.update()

 
        if GUI.loadGaussImageFlag:
            if pathIsSaved:
                GUI.updateText("GAUS show")
                GUI.loadGaussImageFlag=FALSE
                GUI.update()
                imageProcess.showGaussImageImage()
            else:
                GUI.updateText("LOAD PICTUE !")
                GUI.loadGaussImageFlag=FALSE
                GUI.update()

        if GUI.LoadedTestImage:
            if pathIsSaved: 
                GUI.updateText("Original image")
                GUI.LoadedTestImage=FALSE
                GUI.update()
                imageProcess.showLoadedImage()
            else:
                GUI.updateText("LOAD PICTUE !")
                GUI.LoadedTestImage=FALSE
                GUI.update()
        
        if GUI.logImageFlag:
            if pathIsSaved:
                GUI.updateText("Orig. LoG")
                print("volam")
                GUI.logImageFlag=FALSE
                GUI.update()
                imageProcess.getLOGpythonfunctions()
            else:
                GUI.updateText("LOAD PICTUE !")
                GUI.logImageFlag=FALSE
                GUI.update()


        if GUI.closeFlag:
            GUI.destroy()
            break

        GUI.update()
        
        

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()




