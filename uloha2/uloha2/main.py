##################### ZadaniePVSO uloha 2 MAIN #####################
# Autor: Michal Molnar & Tomas Nyiri

from cProfile import label
from pickle import FALSE, TRUE
import appGUI
import cv2
import imageProcessing as imgProc
import matplotlib.pyplot


def main():
    GUI = appGUI.App()
    imageProcess = imgProc.ImgProc(GUI)
    pathIsSaved= FALSE
    GUI.updateText("CHOOS img")
    GUI.update()

    imageProcess.k=1 ## Odskusane velkosti filtra kde k=1;2;4
    imageProcess.slowGauss==False  ## Rychlejsi vypocet gaussiana pomalsi sa zachoval v kode pre porovnanie rychlosti 


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
            imageConverted=imageProcess.imgConvert()
            pathIsSaved= TRUE
            imageProcess.filepathExist=False
            GUI.update()
            GUI.imageIsprocesed=imageProcess.getFalgImageisProcesed()


        if GUI.loadLaplacianimageFlag:
            if pathIsSaved: 
                GUI.updateText("LAP show")
                GUI.loadLaplacianimageFlag=FALSE
                GUI.update()
                imageProcess.showZCImage()
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

        if GUI.GraphFlag:
            if pathIsSaved: 
                GUI.GraphFlag=FALSE
                GUI.update()
                imageProcess.showFIlterGraph()
            else:
                GUI.updateText("LOAD PICTUE !")
                GUI.GraphFlag=FALSE
                GUI.update()
    


        if GUI.logImageFlag:
            if pathIsSaved:
                GUI.updateText("Orig. LoG")
                print("volam")
                GUI.logImageFlag=False
                GUI.update()
                imageProcess.getLOGpythonfunctions()
            else:
                GUI.updateText("LOAD PICTUE !")
                GUI.logImageFlag=False
                GUI.update()


        if GUI.closeFlag:
            GUI.destroy()
            
            break

        GUI.update()
        
        

    cv2.destroyAllWindows()
    matplotlib.pyplot.close('all')


if __name__ == "__main__":
    main()




