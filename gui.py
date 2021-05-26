from PyQt5 import QtCore, QtGui, QtWidgets
import engine
import speech_recog as my_sr
from author_data import email


class GUI_Main_Window(object):
    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Clevera")
        MainWindow.resize(552, 375)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255)")

        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")

        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 551, 351))
        self.tab_widget.setToolTipDuration(-1)
        self.tab_widget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tab_widget.setObjectName("tab_widget")

        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_main")

        self.tab_about = QtWidgets.QWidget()
        self.tab_about.setObjectName("tab_about")

        self.tab_widget.addTab(self.tab_main, "Main")
        self.tab_widget.addTab(self.tab_about, "About me")

        self.label_logo = QtWidgets.QLabel(self.tab_main)
        self.label_logo.setGeometry(QtCore.QRect(90, 10, 321, 91))
        self.label_logo.setAutoFillBackground(False)

        self.label_logo.setPixmap(QtGui.QPixmap("clevera_images/logo_clevera.png"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")

        self.button_speak = QtWidgets.QPushButton(self.tab_main)
        self.button_speak.setGeometry(QtCore.QRect(170, 110, 141, 131))
        self.button_speak.setAutoFillBackground(True)

        icon_speak = QtGui.QIcon()
        icon_speak.addPixmap(QtGui.QPixmap("clevera_images/cl_speak.png"))

        self.button_speak.setIcon(icon_speak)
        self.button_speak.setIconSize(QtCore.QSize(150, 200))
        self.button_speak.setCheckable(False)
        self.button_speak.setAutoExclusive(True)
        self.button_speak.setFlat(True)
        self.button_speak.setObjectName("button_speak")


        self.frame_display_msg = QtWidgets.QFrame(self.tab_main)
        self.frame_display_msg.setGeometry(QtCore.QRect(90, 110, 331, 131))
        self.frame_display_msg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_display_msg.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_display_msg.setObjectName("frame_display_msg")
        self.frame_display_msg.setVisible(False)

        self.label_user_text = QtWidgets.QPlainTextEdit(self.frame_display_msg)
        self.label_user_text.setGeometry(QtCore.QRect(20, 20, 291, 71))
        self.label_user_text.setAutoFillBackground(True)
        self.label_user_text.horizontalScrollBar()
        self.label_user_text.verticalScrollBar()
        self.label_user_text.setReadOnly(True)
        self.label_user_text.setObjectName("label_user_text")

        self.label_clevera_text = QtWidgets.QPlainTextEdit(self.tab_main)
        self.label_clevera_text.setGeometry(QtCore.QRect(110, 252, 291, 71))
        self.label_clevera_text.setAutoFillBackground(True)
        self.label_clevera_text.horizontalScrollBar()
        self.label_clevera_text.verticalScrollBar()
        self.label_clevera_text.setReadOnly(True)
        self.label_clevera_text.setObjectName("label_clevera_text")

        self.label_icon_display = QtWidgets.QLabel(self.tab_main)
        self.label_icon_display.setGeometry(QtCore.QRect(20, 250, 71, 71))
        self.label_icon_display.setAutoFillBackground(True)
        self.label_icon_display.setText("")
        self.label_icon_display.setScaledContents(True)
        self.label_icon_display.setObjectName("label_icon_display")

        self.text_about = QtWidgets.QTextBrowser(self.tab_about)
        self.text_about.setGeometry(QtCore.QRect(50, 70, 431, 241))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.text_about.setFont(font)
        self.text_about.setFrameShape(QtWidgets.QFrame.Box)
        self.text_about.setReadOnly(True)
        self.text_about.setOpenExternalLinks(True)
        self.text_about.setOpenLinks(True)
        self.text_about.setObjectName("text_about")
        basic_style_format = "<span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400;\""
        bold_style_format = "<span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\""
        self.text_about.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body <p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        + basic_style_format +">Hello, I am a simple voice assistant called </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; color:#6600cc;\">Clevera</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400;\">.<br /><br />In </span><span style=\" font-family:\'MS Shell Dlg 2\'; "
        "font-size:10pt; font-weight:400; font-style:italic;\">Main </span>" + basic_style_format + ">section, after clicking a </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:italic;\">microphone</span>"+ basic_style_format+ "> icon, you can ask me something.<br /><br /" +
        ">Possible asks that you can make:<br />- What </span>" + bold_style_format + ">time is</span>"+ basic_style_format+ "> it?<br />- </span>" + bold_style_format+ ">What is</span>" + basic_style_format + "> ...?<br />- </span>" + bold_style_format + ">Who is</span>"+ basic_style_format + "> ...?<br />- </span>" + bold_style_format +
        ">Open Google</span>" + basic_style_format + "><br />- </span>" + bold_style_format + ">Search</span>" + basic_style_format + "> ... </span>" + bold_style_format + ">on Google</span>" + basic_style_format + "><br />- </span>" + bold_style_format +">Open YouTube</span>" + basic_style_format + "><br />- Open ... </span>" + bold_style_format +
        ">on YouTube</span>" + basic_style_format + "><br />- What </span>" + bold_style_format + ">temperature</span>" + basic_style_format + "> is in ...?<br />- What is the </span>" + bold_style_format + ">weather today </span>" + basic_style_format + ">in ...?<br />- Is it </span>" + bold_style_format +">raining today</span>" +basic_style_format +
        ">?<br />- What </span>" + basic_style_format + "> will be the </span>" + bold_style_format + ">day after tomorrow</span>" + basic_style_format + "> in ...?</span>" + bold_style_format + "><br /></span></p>\n"
        "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400;\">The weather forecast is based on the data from </span><a href=\"https://openweathermap.org/api\"><span style=\" font-size:9pt; "
        "text-decoration: underline; color:#6600cc;\">OpenWeather</span></a><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400;\">.</span></p>\n"
        "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-weight:400;\">Contact (by email) to the author: " + email +"<br /></span></p></body></html>")

        self.label_logo_2 = QtWidgets.QLabel(self.tab_about)
        self.label_logo_2.setGeometry(QtCore.QRect(150, 0, 221, 51))
        self.label_logo_2.setAutoFillBackground(False)
        self.label_logo_2.setPixmap(QtGui.QPixmap("clevera_images/logo_clevera.png"))
        self.label_logo_2.setScaledContents(True)
        self.label_logo_2.setObjectName("label_logo_2")

        MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.button_speak.clicked.connect(self.print_message)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def print_message(self):
        self.label_user_text.setPlainText("")
        self.label_clevera_text.setPlainText("")
        self.label_icon_display.setVisible(False)
        self.statusbar.showMessage("")
        self.frame_display_msg.setVisible(True)
        self.label_user_text.setPlainText("You can start speaking in one second :)")
        QtWidgets.QApplication.processEvents()
        err_message = engine.error_and_message()
        error_ = err_message[0]
        message_ = ""
        if error_ == 0:
            message_ = err_message[1]
        else:
            self.statusbar.showMessage("Error number: " + str(error_))

        self.label_user_text.setPlainText("ASK: " + message_)
        QtWidgets.QApplication.processEvents()

        error, result = engine.run(err_message)

        if error != 0:
            self.statusbar.showMessage("Error number: " + str(error_))

        if type(result) == tuple:
            result_msg = result[0]
            result_icon = result[1]
            self.label_icon_display.setVisible(True)
            self.label_icon_display.setPixmap(QtGui.QPixmap(result_icon))
        else:
            result_msg = result
        self.label_clevera_text.setPlainText("RESPONSE: " + result_msg)
        QtWidgets.QApplication.processEvents()

        my_sr.speak(result_msg)

        self.frame_display_msg.setVisible(False)
        QtWidgets.QApplication.processEvents()

    def make_microphone_unclickable(self):
        self.button_speak.setEnabled(False)
        QtWidgets.QApplication.processEvents()

    def make_microphone_clickable(self):
        self.button_speak.setEnabled(True)
        QtWidgets.QApplication.processEvents()
