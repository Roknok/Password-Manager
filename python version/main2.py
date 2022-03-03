from PyQt5.QtWidgets import QLabel,QMainWindow,QApplication,QPushButton,QTextEdit,QLineEdit,QComboBox,QMessageBox
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt
import sys
import json
from random import choice



class Window(QMainWindow):
  
    def __init__(self,passwords):
        super().__init__()
  
        self.setWindowTitle("Password Manager")

        self.setWindowIcon(QIcon("logo.png"))
  
        self.setFixedSize(400,400)
  
        self.UiComponents(passwords)
  
        self.show()

        self.setStyleSheet("Window { background-color:#bababa }  QLabel { color: black } QLineEdit,QTextEdit,QComboBox { background-color:#cfcfcf; color: black; border: 1px solid grey} QPushButton { background-color:#9e9e9e; border: 1px solid grey } QPushButton:hover{ background-color:#909090 }   QPushButton:pressed{ background-color:grey }  QLineEdit:focus,QTextEdit:focus,QComboBox:focus { border:1px solid white; background-color:#dfdfdf }")
        # self.passwords = passwords
  
    def UiComponents(self,passwords):

        label = QLabel("Password Manager",self)
        label.setGeometry(15,15,400-30,45)
        label.setFont(QFont('calibri', 30))
        label.setAlignment(Qt.AlignCenter)
        def copyPassword():
            textarea.setFocus()
            textarea.copy()

        button2 = QPushButton('Copy', self)
        button2.setGeometry(15+300,250+80,100-30,35)
        button2.clicked.connect(copyPassword)
        button2.setFont(QFont('calibri', 15))
    
        def removePassword():
            if combo_box.currentText() != "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText('Do you REALLY want to delete "'+combo_box.currentText()+'"')
                msg.setWindowTitle("Attention !")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.setWindowIcon(QIcon("logo.png"))
                retval = msg.exec_()
                if retval == 1024:
                    passwords.pop(combo_box.currentText())
                    save()
                    combo_box.clear()
                    for i in passwords:
                        combo_box.addItem(i)


        button3 = QPushButton('Delete', self)
        button3.setGeometry(15+300,200+80,100-30,35)
        button3.clicked.connect(removePassword)
        button3.setFont(QFont('calibri', 15))

        textarea = QTextEdit(self)
        textarea.setGeometry(15,250+80,300-15,35)
        textarea.setText("— — — — — — — —")
        textarea.setAlignment(Qt.AlignCenter)
        textarea.setFont(QFont('calibri', 15))
        textarea.setReadOnly(True)

        textbox = QLineEdit(self)
        textbox.setGeometry(15,15+70,400-30,35)
        textbox.setPlaceholderText("Name") 
        textbox.setFont(QFont('calibri', 15))

        textbox2 = QLineEdit(self)
        textbox2.setGeometry(15,15+40+15+70,350-30,35)
        textbox2.setPlaceholderText("Password") 
        textbox2.setFont(QFont('calibri', 15))

        def generatePassword():
            chr1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`'"
            chr2 = '!@#$%^&*()_-+={[}]|\:;"<,>.?/'
            characters = chr1+chr2
            psw = ""
            for i in range(0,10):
                psw += choice(characters)
            textbox2.setText(psw)


        button4 = QPushButton('G', self)
        button4.setGeometry(350,15+40+15+70,50-15,35)
        button4.clicked.connect(generatePassword)
        button4.setFont(QFont('calibri', 15))
        

        def save():
            file = open('passwords.json','w')
            file.write(json.dumps(passwords))

        def addPassword():
            do = True
            for i in passwords:
                if i == textbox.text():


                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("The name of the password you wanted to save already exists! \n Replace the original password?")
                    msg.setWindowTitle("Attention !")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.setWindowIcon(QIcon("logo.png"))
                    retval = msg.exec_()
                    if retval == 1024:
                        passwords[textbox.text()] = textbox2.text()
                        save()
                        textarea.setText(passwords[combo_box.currentText()])
                    do = False
            

            if textbox.text().isspace() or textbox.text() == "" or textbox2.text().isspace() or textbox2.text() == "":
                do = False

            if do:
                passwords[textbox.text()] = textbox2.text()
                combo_box.addItem(textbox.text())
                save()


        button = QPushButton('Add', self)
        button.setGeometry(15,15+40+15+40+15+70,400-30,35)
        button.clicked.connect(addPassword)
        button.setFont(QFont('calibri', 15))

        def updatePassword():
            if combo_box.currentText() != "":
                textarea.setText(passwords[combo_box.currentText()])
            else:
                textarea.setText("— — — — — — — —")
                textarea.setAlignment(Qt.AlignCenter)
        
        combo_box = QComboBox(self)
        combo_box.setGeometry(15,200+80,300-15,35)
        combo_box.setFont(QFont('calibri', 15))
        combo_box.currentIndexChanged.connect(updatePassword)
        for i in passwords:
            combo_box.addItem(i)



App = QApplication(sys.argv)

file = open("passwords.json","r")
passwords = json.load(file)

window = Window(passwords)

sys.exit(App.exec())