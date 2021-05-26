from internet_connection import isConnectedToInternet
import engine
import gui

if __name__ == "__main__":
    import sys
    app = gui.QtWidgets.QApplication(sys.argv)
    MainWindow = gui.QtWidgets.QMainWindow()
    gui = gui.GUI_Main_Window()
    gui.setup(MainWindow)
    MainWindow.show()
    gui.make_microphone_unclickable()
    engine.introduction()
    gui.make_microphone_clickable()
    if not isConnectedToInternet():
        gui.label_clevera_text.setPlainText("The speech recognition won't work without Internet connection.")
    else:
        gui.label_clevera_text.setPlainText("If you want to say something, press the microphone above :)")
    sys.exit(app.exec_())

