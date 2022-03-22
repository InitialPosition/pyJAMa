# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_create.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConfigCreator(object):
	def setupUi(self, ConfigCreator):
		if not ConfigCreator.objectName():
			ConfigCreator.setObjectName(u"ConfigCreator")
		ConfigCreator.resize(700, 300)
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(ConfigCreator.sizePolicy().hasHeightForWidth())
		ConfigCreator.setSizePolicy(sizePolicy)
		ConfigCreator.setMinimumSize(QSize(700, 300))
		ConfigCreator.setMaximumSize(QSize(700, 300))
		self.verticalLayout = QVBoxLayout(ConfigCreator)
		self.verticalLayout.setObjectName(u"verticalLayout")
		self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

		self.verticalLayout.addItem(self.verticalSpacer_2)

		self.label_explanation = QLabel(ConfigCreator)
		self.label_explanation.setObjectName(u"label_explanation")

		self.verticalLayout.addWidget(self.label_explanation, 0, Qt.AlignLeft | Qt.AlignTop)

		self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

		self.verticalLayout.addItem(self.verticalSpacer_3)

		self.horizontalLayout = QHBoxLayout()
		self.horizontalLayout.setObjectName(u"horizontalLayout")
		self.label_sids = QLabel(ConfigCreator)
		self.label_sids.setObjectName(u"label_sids")

		self.horizontalLayout.addWidget(self.label_sids)

		self.text_sids = QLineEdit(ConfigCreator)
		self.text_sids.setObjectName(u"text_sids")

		self.horizontalLayout.addWidget(self.text_sids)

		self.verticalLayout.addLayout(self.horizontalLayout)

		self.btn_ok = QPushButton(ConfigCreator)
		self.btn_ok.setObjectName(u"btn_ok")

		self.verticalLayout.addWidget(self.btn_ok)

		self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

		self.verticalLayout.addItem(self.verticalSpacer)

		self.retranslateUi(ConfigCreator)

		QMetaObject.connectSlotsByName(ConfigCreator)

	# setupUi

	def retranslateUi(self, ConfigCreator):
		ConfigCreator.setWindowTitle(QCoreApplication.translate("ConfigCreator", u"Form", None))
		self.label_explanation.setText(QCoreApplication.translate("ConfigCreator", u"TextLabel", None))
		self.label_sids.setText(QCoreApplication.translate("ConfigCreator", u"TextLabel", None))
		self.btn_ok.setText(QCoreApplication.translate("ConfigCreator", u"PushButton", None))
# retranslateUi
