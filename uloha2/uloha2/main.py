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


    while True:
        
        if GUI.path:
            GUI.updateText("Image is loaded")
            GUI.update()
            imageProcess.buttonSetPathClicked()
            GUI.path=False

        if GUI.loadDEFAULTimageFlag:
            GUI.updateText("Image is loaded")
            GUI.update()
            imageProcess.loadTESTimage()
            GUI.loadDEFAULTimageFlag=False


        if imageProcess.filepathExist: 
            GUI.updateText("Image is loaded") 
            GUI.pictureHight,GUI.pictureWidth,imageConverted=imageProcess.imgConvert()
            GUI.update()
            #GUI.picture.configure(image=imageConverted)
            imageProcess.filepathExist=False
            GUI.imageIsprocesed=imageProcess.getFalgImageisProcesed()

        if GUI.loadLaplacianimageFlag:
            GUI.updateText("Image is loaded")
            GUI.update()
            imageProcess.showLaplacianOriginalImage()
            GUI.loadLaplacianimageFlag=FALSE

        if GUI.loadGaussImageFlag:
            GUI.updateText("Image is loaded")
            GUI.update()
            imageProcess.showGaussImageImage()
            GUI.loadGaussImageFlag=FALSE

        if GUI.LoadedTestImage:
            GUI.updateText("Image is loaded")
            GUI.update()
            imageProcess.showLoadedImage()
            GUI.LoadedTestImage=FALSE
        
        if GUI.logImageFlag:
            GUI.updateText("Orig. LoG")
            GUI.update()
            print("volam")
            imageProcess.getLOGpythonfunctions()
            GUI.logImageFlag=FALSE

        if GUI.closeFlag:
            GUI.destroy()
            break

        GUI.update()
        
        

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()




