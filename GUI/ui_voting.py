# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'voting.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *


class Ui_VotingWindow(object):
	def setupUi(self, VotingWindow):
		if not VotingWindow.objectName():
			VotingWindow.setObjectName(u"VotingWindow")
		VotingWindow.resize(1000, 700)
		VotingWindow.setMinimumSize(QSize(1000, 700))
		VotingWindow.setMaximumSize(QSize(16777214, 16777215))
		self.actionAbout_pyJAMa = QAction(VotingWindow)
		self.actionAbout_pyJAMa.setObjectName(u"actionAbout_pyJAMa")
		self.actionCheck_for_Updates = QAction(VotingWindow)
		self.actionCheck_for_Updates.setObjectName(u"actionCheck_for_Updates")
		self.actionInput_token = QAction(VotingWindow)
		self.actionInput_token.setObjectName(u"actionInput_token")
		self.actionTest_Connection = QAction(VotingWindow)
		self.actionTest_Connection.setObjectName(u"actionTest_Connection")
		self.actionReload_all_Data = QAction(VotingWindow)
		self.actionReload_all_Data.setObjectName(u"actionReload_all_Data")
		self.actionQuit = QAction(VotingWindow)
		self.actionQuit.setObjectName(u"actionQuit")
		self.centralwidget = QWidget(VotingWindow)
		self.centralwidget.setObjectName(u"centralwidget")
		self.verticalLayout = QVBoxLayout(self.centralwidget)
		self.verticalLayout.setObjectName(u"verticalLayout")
		self.label_status = QLabel(self.centralwidget)
		self.label_status.setObjectName(u"label_status")

		self.verticalLayout.addWidget(self.label_status)

		self.text_theme_search = QLineEdit(self.centralwidget)
		self.text_theme_search.setObjectName(u"text_theme_search")

		self.verticalLayout.addWidget(self.text_theme_search)

		self.list_themes = QListWidget(self.centralwidget)
		self.list_themes.setObjectName(u"list_themes")

		self.verticalLayout.addWidget(self.list_themes)

		self.horizontalLayout = QHBoxLayout()
		self.horizontalLayout.setObjectName(u"horizontalLayout")
		self.btn_vote_yes = QPushButton(self.centralwidget)
		self.btn_vote_yes.setObjectName(u"btn_vote_yes")

		self.horizontalLayout.addWidget(self.btn_vote_yes)

		self.btn_vote_no = QPushButton(self.centralwidget)
		self.btn_vote_no.setObjectName(u"btn_vote_no")

		self.horizontalLayout.addWidget(self.btn_vote_no)

		self.btn_flag = QPushButton(self.centralwidget)
		self.btn_flag.setObjectName(u"btn_flag")

		self.horizontalLayout.addWidget(self.btn_flag)

		self.verticalLayout.addLayout(self.horizontalLayout)

		VotingWindow.setCentralWidget(self.centralwidget)
		self.menubar = QMenuBar(VotingWindow)
		self.menubar.setObjectName(u"menubar")
		self.menubar.setGeometry(QRect(0, 0, 1000, 21))
		VotingWindow.setMenuBar(self.menubar)
		self.statusbar = QStatusBar(VotingWindow)
		self.statusbar.setObjectName(u"statusbar")
		VotingWindow.setStatusBar(self.statusbar)

		self.retranslateUi(VotingWindow)

		QMetaObject.connectSlotsByName(VotingWindow)

	# setupUi

	def retranslateUi(self, VotingWindow):
		VotingWindow.setWindowTitle(QCoreApplication.translate("VotingWindow", u"MainWindow", None))
		self.actionAbout_pyJAMa.setText(QCoreApplication.translate("VotingWindow", u"About pyJAMa", None))
		self.actionCheck_for_Updates.setText(QCoreApplication.translate("VotingWindow", u"Check for Updates", None))
		self.actionInput_token.setText(QCoreApplication.translate("VotingWindow", u"Input Token", None))
		self.actionTest_Connection.setText(QCoreApplication.translate("VotingWindow", u"Test Connection", None))
		self.actionReload_all_Data.setText(QCoreApplication.translate("VotingWindow", u"Reload all Data", None))
		self.actionQuit.setText(QCoreApplication.translate("VotingWindow", u"Quit", None))
		self.label_status.setText(QCoreApplication.translate("VotingWindow", u"TextLabel", None))
		self.text_theme_search.setPlaceholderText(
			QCoreApplication.translate("VotingWindow", u"Search for Themes", None))
		self.btn_vote_yes.setText(QCoreApplication.translate("VotingWindow", u"Vote YES", None))
		self.btn_vote_no.setText(QCoreApplication.translate("VotingWindow", u"Vote NO", None))
		self.btn_flag.setText(QCoreApplication.translate("VotingWindow", u"FLAG", None))
# retranslateUi
