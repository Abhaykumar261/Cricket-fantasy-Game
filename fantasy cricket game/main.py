# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cricket_fantasy.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from evaluation import evaluate

class Ui_MainWindow(object):
    def __init__(self):
        self.count_BAT=0
        self.count_WK=0
        self.count_BOW=0
        self.count_AR=0
        self.PointAvl=1000
        self.Pointused=0
        self.teams=set()
        self.AllTeams=[]
        self.playersSelectedList=[]

    # Sql command for Connecting FantasyCricket Database
    def connectdb(self):
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        return objcricket

    # Method for displaying BatsMan in ListWidget(players_list)
    def BAT_players(self):
        objcricket=self.connectdb()
        self.players_list.clear()
        objcricket.execute('Select Player from Stats where ctg="BAT" ')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.players_list.addItem(i[0])

    # Method for displaying Bowlers in ListWidget(playersList)
    def BOW_players(self):
        objcricket=self.connectdb()
        self.players_list.clear()
        objcricket.execute('Select Player from Stats where ctg="BOW" ')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.players_list.addItem(i[0])

    # Method for displaying AllRounders in ListWidget(playersList)
    def AR_players(self):
        objcricket=self.connectdb()
        self.players_list.clear()
        objcricket.execute('Select Player from Stats where ctg="AR" ')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.players_list.addItem(i[0])

    # Method for showing WicketKeeper in ListWidget
    def WK_players(self):
        objcricket=self.connectdb()
        self.players_list.clear()
        objcricket.execute('Select Player from Stats where ctg="WK" ')
        for i in objcricket.fetchall():
            if i[0] not in self.playersSelectedList:
                self.players_list.addItem(i[0])

    # Method for Creating a New Team
    def new_team(self):
        self.messagebox('Welcome','''Please Enter Team Name in the Team Name section\n(Choose 11 Players Precisely)''')
        self.players_list.clear()
        self.selected_players.clear()
        self.playersSelectedList=[]
        self.count_BAT=0
        self.count_WK=0
        self.count_BOW=0
        self.count_AR=0
        self.PointAvl=1000
        self.Pointused=0
        self.WK.clicked.connect(self.WK_players) # ----------- WK Button
        self.BAT.clicked.connect(self.BAT_players) #--------BAT BUTTON
        self.BOW.clicked.connect(self.BOW_players) #=-------BOW BUTTON
        self.AR.clicked.connect(self.AR_players) #--------AR BUTTON
        self.team_name.clear()
        self.team_name.setPlaceholderText("Enter Name")
        self.points_avail.setText("1000")
        self.points_used.setText("0")
        self.AR_count.setText("0")
        self.WK_count.setText("0")
        self.BOW_count.setText("0")
        self.BAT_count.setText("0")

    # Method for Opening Team
    def open_team(self):
        self.teams=set()
        self.playersSelectedList=[]
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('Select Name from Teams')
        rows= objcricket.fetchall()
        for row in rows:
            self.teams.add(row[0])
        self.team, ok=QtWidgets.QInputDialog.getItem(MainWindow,"Open","Choose A Team",self.teams,0,False)
        if ok == True:
            self.team_name.setText(self.team)
            self.points_avail.setText("1000")
            self.points_used.setText("0")
            self.AR_count.setText("0")
            self.WK_count.setText("0")
            self.BOW_count.setText("0")
            self.BAT_count.setText("0")
            self.selected_players.clear()
            self.players_list.clear()
            self.count_BAT=0
            self.count_WK=0
            self.count_BOW=0
            self.count_AR=0
            self.PointAvl=1000
            self.Pointused=0
            self.AllTeams=[]
            self.WK.clicked.connect(self.WK_players) # ----------- WK Button
            self.BAT.clicked.connect(self.BAT_players) #--------BAT BUTTON
            self.BOW.clicked.connect(self.BOW_players) #=-------BOW BUTTON
            self.AR.clicked.connect(self.AR_players) #--------AR BUTTON
                
            objcricket=self.connectdb()
            objcricket.execute('Select Player,Name,value from Teams')
            for i in objcricket.fetchall():
                if i[1] == self.team:
                    self.Pointused+=i[2]
                    self.points_used.setText(str(self.Pointused))
                    self.points_avail.setText(str(self.PointAvl-self.Pointused))
                    self.selected_players.addItem(i[0])
                    self.playersSelectedList.append(i[0])
                    
            objcricket.execute('Select Player,ctg from Stats')
            for i in objcricket.fetchall():
                if i[0] in self.playersSelectedList:
                    if i[1] == 'WK':
                        self.count_WK+=1
                        self.WK_count.setText(str(self.count_WK))
                    if i[1] == 'BOW':
                        self.count_BOW+=1
                        self.BOW_count.setText(str(self.count_BOW))
                    if i[1] == 'AR':
                        self.count_AR+=1
                        self.AR_count.setText(str(self.count_AR))
                    if i[1] == 'BAT':
                        self.count_BAT+=1
                        self.BAT_count.setText(str(self.count_BAT))
        else: pass

    # Method for Saving Team
    def save_team(self):
        cricket=sqlite3.connect('fantasycricket.db')
        objcricket=cricket.cursor()
        objcricket.execute('Select Name from Teams')
        self.teamlist=[]
        if self.team_name.text() !="":
            if self.selected_players.count() == 11:
                for i in objcricket.fetchall():
                    self.teamlist.append(i[0])
                objcricket.execute('Select Player,ctg,value from Stats')
                if self.team_name.text() not in self.teamlist:
                    for i in objcricket.fetchall():
                        if i[0] in self.playersSelectedList:
                            objcricket.execute('''INSERT INTO Teams(Player,Name,value)
                            values("%s","%s","%i")'''%(i[0],self.team_name.text(),i[2]))
                            cricket.commit()
                    self.messagebox('Hurry',"%s Team Saved Successfully"%(self.team_name.text()))
                    self.players_list.clear()
                    self.selected_players.clear()
                    self.playersSelectedList=[]
                    self.count_BAT=0
                    self.count_WK=0
                    self.count_BOW=0
                    self.count_AR=0
                    self.PointAvl=1000
                    self.Pointused=0
                    self.team_name.clear()
                    self.team_name.setPlaceholderText("Enter Name")
                    self.points_avail.setText("1000")
                    self.points_used.setText("0")
                    self.AR_count.setText("0")
                    self.WK_count.setText("0")
                    self.BOW_count.setText("0")
                    self.BAT_count.setText("0")
                else:
                    self.messagebox('Sorry','%s Team Already Exist.\n(If You Want to Modify Team, Delete it and Save Modified Team)'%(self.team_name.text()))
            else:
                self.messagebox('Error','There Should be 11 Players')
        else:
            self.messagebox('Error','Please Enter Team Name')
   
   # Opening Imported file for evaluation
    def openEvaluate(self):
        self.window=QtWidgets.QWidget()
        self.ui= evaluate.Ui_evaluate()
        self.ui.setupUi(self.window)
        self.window.show()

    # Removing and adding Players in the ListWidget from PlayersList to SeletedPlayers
    def removePlayersList(self,item):
        objcricket=self.connectdb()
        objcricket.execute('select Player,ctg,value from Stats')
        if self.selected_players.count()<12:
            self.players_list.takeItem(self.players_list.row(item))
            if item.text() not in self.playersSelectedList:
                for i in objcricket.fetchall(): 
                    if item.text() == i[0]:
                        if self.PointAvl >= i[2]:
                            if i[1] == 'BAT':
                                self.count_BAT+=1
                                self.BAT_count.setText("%s"%(self.count_BAT))
                                self.selected_players.addItem(item.text())
                                self.playersSelectedList.append(item.text())
                            elif i[1] == "WK":
                                self.count_WK+=1
                                if self.count_WK<=1:
                                    self.WK_count.setText('%s'%(self.count_WK))
                                    self.selected_players.addItem(item.text())
                                    self.playersSelectedList.append(item.text())
                                elif self.count_WK==2:
                                    self.messagebox('Warning', "You can't select more than 1 Wicket Keeper")
                                    break
                            elif i[1] == 'AR':
                                self.count_AR+=1
                                self.AR_count.setText('%s'%(self.count_AR))
                                self.selected_players.addItem(item.text())
                                self.playersSelectedList.append(item.text())
                            elif i[1] == 'BOW':
                                self.count_BOW+=1
                                self.BOW_count.setText('%s'%(self.count_BOW))
                                self.selected_players.addItem(item.text())
                                self.playersSelectedList.append(item.text()) 
                            self.PointAvl-=i[2]
                            self.Pointused+=i[2]
                            self.points_avail.setText(str(self.PointAvl))
                            self.points_used.setText(str(self.Pointused))
                        elif self.PointAvl < i[2]:
                            self.messagebox('Warning',"You don't you have enough Points")
                            break
            else:
                self.messagebox('Warning',"You Can't select same Player Again")
        else:
            self.messagebox('Warning',"You can't select more than 11 Players")

    # Removing and adding Players in the ListWidget from SeletedPlayers to PlayersList 
    def removeSelectedPlayers(self,item):
        self.PointAvl=int(self.points_avail.text())
        objcricket=self.connectdb()
        objcricket.execute('select Player,ctg,value from Stats')
        self.selected_players.takeItem(self.selected_players.row(item))
        for i in objcricket.fetchall():
            c=i[2]  
            if item.text()==i[0]:
                if i[1] == 'BAT':
                    self.count_BAT-=1
                    self.BAT_count.setText("%s"%(self.count_BAT))
                    self.playersSelectedList.remove(item.text())
                elif i[1] == "WK":
                    self.count_WK=0
                    self.WK_count.setText('%s'%(self.count_WK))
                    self.playersSelectedList.remove(item.text())
                elif i[1] == 'AR':
                    self.count_AR-=1
                    self.AR_count.setText('%s'%(self.count_AR))
                    self.playersSelectedList.remove(item.text())
                elif i[1] == 'BOW':
                    self.count_BOW-=1
                    self.BOW_count.setText('%s'%(self.count_BOW))
                    self.playersSelectedList.remove(item.text())
                self.PointAvl+=c
                self.Pointused-=c
                self.points_avail.setText(str(self.PointAvl))
                self.points_used.setText(str(self.Pointused))

    # Message box
    def messagebox(self,title,message):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.setStyleSheet("background-color: #E0FFFF")
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        mess.setFont(font)
        mess.exec_()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setUnderline(True)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 4, 8, 1, 1)
        self.BAT_count = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setUnderline(False)
        self.BAT_count.setFont(font)
        self.BAT_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BAT_count.setText("")
        self.BAT_count.setObjectName("BAT_count")
        self.gridLayout.addWidget(self.BAT_count, 1, 1, 1, 1)
        self.points_used = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setUnderline(False)
        self.points_used.setFont(font)
        self.points_used.setFrameShape(QtWidgets.QFrame.Box)
        self.points_used.setText("")
        self.points_used.setObjectName("points_used")
        self.gridLayout.addWidget(self.points_used, 3, 9, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        font.setUnderline(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 8, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 3, 8, 1, 1)
        self.selected_players = QtWidgets.QListWidget(self.centralwidget)
        self.selected_players.setObjectName("selected_players")
        self.gridLayout.addWidget(self.selected_players, 5, 8, 1, 5)
        self.BOW = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.BOW.setFont(font)
        self.BOW.setObjectName("BOW")
        self.gridLayout.addWidget(self.BOW, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        font.setUnderline(False)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 4, 1, 1)
        self.BAT = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.BAT.setFont(font)
        self.BAT.setObjectName("BAT")
        self.gridLayout.addWidget(self.BAT, 4, 0, 1, 1)
        self.AR_count = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(False)
        self.AR_count.setFont(font)
        self.AR_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.AR_count.setText("")
        self.AR_count.setObjectName("AR_count")
        self.gridLayout.addWidget(self.AR_count, 1, 9, 1, 1)
        self.WK_count = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setUnderline(False)
        self.WK_count.setFont(font)
        self.WK_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.WK_count.setText("")
        self.WK_count.setObjectName("WK_count")
        self.gridLayout.addWidget(self.WK_count, 1, 12, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 13)
        self.players_list = QtWidgets.QListWidget(self.centralwidget)
        self.players_list.setObjectName("players_list")
        self.gridLayout.addWidget(self.players_list, 5, 0, 1, 7)
        self.team_name = QtWidgets.QLineEdit(self.centralwidget)
        self.team_name.setObjectName("team_name")
        self.gridLayout.addWidget(self.team_name, 4, 9, 1, 2)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 5, 7, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        font.setUnderline(False)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 11, 1, 1)
        self.BOW_count = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setUnderline(False)
        self.BOW_count.setFont(font)
        self.BOW_count.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BOW_count.setText("")
        self.BOW_count.setObjectName("BOW_count")
        self.gridLayout.addWidget(self.BOW_count, 1, 5, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        font.setKerning(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.points_avail = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setUnderline(False)
        self.points_avail.setFont(font)
        self.points_avail.setFrameShape(QtWidgets.QFrame.Box)
        self.points_avail.setText("")
        self.points_avail.setObjectName("points_avail")
        self.gridLayout.addWidget(self.points_avail, 3, 1, 1, 1)
        self.WK = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.WK.setFont(font)
        self.WK.setObjectName("WK")
        self.gridLayout.addWidget(self.WK, 4, 5, 1, 1)
        self.AR = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setUnderline(False)
        self.AR.setFont(font)
        self.AR.setObjectName("AR")
        self.gridLayout.addWidget(self.AR, 4, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuManage_Team = QtWidgets.QMenu(self.menubar)
        self.menuManage_Team.setObjectName("menuManage_Team")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Team = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setKerning(True)
        self.actionNew_Team.setFont(font)
        self.actionNew_Team.setObjectName("actionNew_Team")
        self.actionOpen_Team = QtWidgets.QAction(MainWindow)
        self.actionOpen_Team.setObjectName("actionOpen_Team")
        self.actionSave_Team = QtWidgets.QAction(MainWindow)
        self.actionSave_Team.setObjectName("actionSave_Team")
        self.actionEvaluate_Team = QtWidgets.QAction(MainWindow)
        self.actionEvaluate_Team.setObjectName("actionEvaluate_Team")
        self.menuManage_Team.addAction(self.actionNew_Team)
        self.menuManage_Team.addAction(self.actionOpen_Team)
        self.menuManage_Team.addAction(self.actionSave_Team)
        self.menuManage_Team.addAction(self.actionEvaluate_Team)
        self.menubar.addAction(self.menuManage_Team.menuAction())

        #============= Connecting All Action methods===========<<
        self.actionSave_Team.triggered.connect(self.save_team)
        self.actionNew_Team.triggered.connect(self.new_team)
        self.actionOpen_Team.triggered.connect(self.open_team)
        self.actionEvaluate_Team.triggered.connect(self.openEvaluate)
        self.players_list.itemDoubleClicked.connect(self.removePlayersList)     # Connecting Method removePlayersList 
        self.selected_players.itemDoubleClicked.connect(self.removeSelectedPlayers)  # Connecting Method SelectedPlayers

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_14.setText(_translate("MainWindow", "Team Name :"))
        self.label_6.setText(_translate("MainWindow", "Allrounders(AR)"))
        self.label_12.setText(_translate("MainWindow", "Points Used :"))
        self.BOW.setText(_translate("MainWindow", "BOW"))
        self.label_4.setText(_translate("MainWindow", "Bowlers(BOW)"))
        self.BAT.setText(_translate("MainWindow", "BAT"))
        self.label_2.setText(_translate("MainWindow", "Batsmen(BAT)"))
        self.label.setText(_translate("MainWindow", "Your Selections"))
        self.label_15.setText(_translate("MainWindow", ">>"))
        self.label_8.setText(_translate("MainWindow", "Wicket-Keepers(WK)"))
        self.label_10.setText(_translate("MainWindow", "Points Available :"))
        self.WK.setText(_translate("MainWindow", "WK"))
        self.AR.setText(_translate("MainWindow", "AR"))
        self.menuManage_Team.setTitle(_translate("MainWindow", "Manage Team"))
        self.actionNew_Team.setText(_translate("MainWindow", "New Team"))
        self.actionNew_Team.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen_Team.setText(_translate("MainWindow", "Open Team"))
        self.actionOpen_Team.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave_Team.setText(_translate("MainWindow", "Save Team"))
        self.actionSave_Team.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionEvaluate_Team.setText(_translate("MainWindow", "Evaluate Team"))
        self.actionEvaluate_Team.setShortcut(_translate("MainWindow", "Ctrl+E"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
