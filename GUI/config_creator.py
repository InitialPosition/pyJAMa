import os

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QWidget, QMainWindow

from GUI import Styling
from GUI.ui_config_create import Ui_ConfigCreator
from util import Config


class ConfigCreator(QWidget):
	main_window = None

	def __init__(self):
		super().__init__()

		self.ui = Ui_ConfigCreator()
		self.ui.setupUi(self)

		Styling.set_style(self)

		self.setWindowTitle("Enter your Token")

		cookie_explanation = ""
		with open(os.path.join(os.path.realpath(__file__), "../../files/cookie_explanation.txt"), 'r', encoding='utf8') as f:
			for line in f.read().splitlines():
				cookie_explanation += line + "\n"

		self.ui.label_sids.setText("SIDS Token: ")
		self.ui.label_explanation.setText(cookie_explanation)

		self.ui.btn_ok.setText("CONFIRM")
		self.ui.btn_ok.pressed.connect(self.ok_pressed)

		# dark mode options
		dark_mode_enabled = Config.load_config_key(Config.ConfigKeys.DARK_MODE.value)
		if dark_mode_enabled is None:
			dark_mode_enabled = True

		if dark_mode_enabled:
			# style items
			palette = QPalette()
			palette.setColor(QPalette.Text, Qt.white)

			self.ui.text_sids.setPalette(palette)

	def set_main_window(self, window: QMainWindow):
		self.main_window = window

	def ok_pressed(self):
		Config.save_config(self.ui.text_sids.text())

		self.main_window.refresh_theme_list()
		self.main_window.show()

		self.close()
