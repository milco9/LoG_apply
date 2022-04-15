##################### ZadaniePVSO uloha 2 MAIN #####################
# Autor: Michal Molnar & Tomas Nyiri

from cProfile import label
import appGUI
import imageProcessing as imgProc


if __name__ == "__main__":
    defaultPicture= "No Tracking"
    GUI = appGUI.App()
    imageProcess = imgProc.ImgProc(GUI)


    while True:
        
        if GUI.path:
            imageProcess.buttonSetPathClicked()
            GUI.path=False
        if GUI.loadTESTimageFlag:
            imageProcess.loadTESTimage()
            GUI.loadTESTimageFlag=False
        if imageProcess.filepathExist:   
            GUI.picture.configure(image=imageProcess.imgConvert())
            imageProcess.filepathExist=False
            GUI.imageIsprocesed=imageProcess.getFalgImageisProcesed()
        GUI.update()
        if 0xFF == ord('q'):
            break



