import json
import sys
import time

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QMainWindow, QApplication, QAbstractItemView

from GUI import Styling
from GUI.config_creator import ConfigCreator
from GUI.ui_voting import Ui_VotingWindow
from LDJAM_API import LDJAM_API
from util import Config


class VotingWindow(QMainWindow):
	theme_library = None
	voted_themes = None

	config_window = None

	def __init__(self):
		super().__init__()

		self.ui = Ui_VotingWindow()
		self.ui.setupUi(self)

		Styling.set_style(self)

		self.setWindowTitle("pyJAMa by RedCocoa")

		self.event_id = LDJAM_API.get_current_event_id()

		self.ui.list_themes.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ui.list_themes.itemSelectionChanged.connect(self.theme_selection_changed)

		self.ui.text_theme_search.textChanged.connect(self.search_term_changed)

		self.ui.btn_vote_yes.clicked.connect(lambda: self.vote_selected_themes("yes"))
		self.ui.btn_vote_no.clicked.connect(lambda: self.vote_selected_themes("no"))
		self.ui.btn_flag.clicked.connect(lambda: self.vote_selected_themes("flag"))

		self.ui.btn_vote_yes.setEnabled(False)
		self.ui.btn_vote_no.setEnabled(False)
		self.ui.btn_flag.setEnabled(False)

		# dark mode options
		dark_mode_enabled = Config.load_config_key(Config.ConfigKeys.DARK_MODE.value)
		if dark_mode_enabled is None:
			dark_mode_enabled = True

		if dark_mode_enabled:
			# style items
			palette = QPalette()
			palette.setColor(QPalette.Text, Qt.white)

			self.ui.text_theme_search.setPalette(palette)
			self.ui.list_themes.setPalette(palette)

	def search_term_changed(self):
		self.ui.list_themes.clear()

		for theme in self.theme_library['ideas']:
			if theme not in self.voted_themes and self.ui.text_theme_search.text().upper() in self.theme_library[
				'ideas'].get(theme).upper():
				current_theme = self.theme_library['ideas'].get(theme)
				self.ui.list_themes.addItem(current_theme)

		self.ui.list_themes.sortItems()

		if len(self.ui.text_theme_search.text()) > 0:
			self.ui.label_status.setText(
				f"{len(self.theme_library['ideas'])} themes loaded, {len(self.theme_library['ideas']) - len(self.voted_themes)} unvoted ({self.ui.list_themes.count()} filtered)")
		else:
			self.ui.label_status.setText(
				f"{len(self.theme_library['ideas'])} themes loaded, {len(self.theme_library['ideas']) - len(self.voted_themes)} unvoted")

	def theme_selection_changed(self):
		selected_themes = self.ui.list_themes.selectedItems()

		self.ui.btn_flag.setEnabled(True)
		self.ui.btn_vote_no.setEnabled(True)
		self.ui.btn_vote_yes.setEnabled(True)

		if len(selected_themes) == 0:
			self.ui.btn_flag.setEnabled(False)
			self.ui.btn_vote_no.setEnabled(False)
			self.ui.btn_vote_yes.setEnabled(False)

		if len(selected_themes) == 1:
			self.ui.btn_flag.setEnabled(True)
		else:
			self.ui.btn_flag.setEnabled(False)

	def get_theme_id(self, theme_name: str) -> int:
		for theme_id_ in self.theme_library['ideas']:
			if self.theme_library['ideas'].get(theme_id_) == theme_name:
				return theme_id_

		return -1

	def vote_theme(self, theme: str, voting: str) -> None:
		theme_id = self.get_theme_id(theme)
		print(
			f"Vote: {voting}, Theme ID: {theme_id} (To be clear, that is '{self.theme_library['ideas'].get(theme_id)}')")
		voting_success = LDJAM_API.vote_theme(theme_id, voting)

		if voting_success != 0:
			print("Error voting")

	def vote_selected_themes(self, voting: str):
		self.ui.btn_vote_yes.setEnabled(False)
		self.ui.btn_vote_no.setEnabled(False)
		self.ui.btn_flag.setEnabled(False)

		self.ui.list_themes.setEnabled(False)
		self.ui.text_theme_search.setEnabled(False)

		counter = 0
		theme_count = len(self.ui.list_themes.selectedItems())
		for theme in self.ui.list_themes.selectedItems():
			self.vote_theme(theme.text(), voting)

			counter += 1
			theme.setText(f"{theme.text()}    ({'Voted ' + voting.upper() if voting != 'flag' else 'FLAGGED'})")
			self.ui.label_status.setText(
				f"Voting... {round((counter / theme_count) * 100)}% done ({counter} / {theme_count})")
			QtCore.QCoreApplication.processEvents()

			time.sleep(1)

		self.ui.text_theme_search.clear()
		self.refresh_theme_list()

		self.ui.list_themes.setEnabled(True)
		self.ui.text_theme_search.setEnabled(True)
		self.ui.text_theme_search.clear()

	def refresh_theme_list(self):
		request = LDJAM_API.get_event_themes(self.event_id)
		self.theme_library = json.loads(request.text)
		self.voted_themes = LDJAM_API.get_user_votes(self.event_id)

		self.ui.label_status.setText(
			f"{len(self.theme_library['ideas'])} themes loaded, {len(self.theme_library['ideas']) - len(self.voted_themes)} unvoted")
		self.ui.label_status.setStyleSheet("font-size: 15pt;")

		self.ui.list_themes.clear()

		for theme in self.theme_library['ideas']:
			if theme not in self.voted_themes:
				current_theme = self.theme_library['ideas'].get(theme)
				self.ui.list_themes.addItem(current_theme)

		self.ui.list_themes.sortItems()


app = QApplication([])

voting_window = VotingWindow()

if Config.has_config():
	voting_window.refresh_theme_list()
	voting_window.show()
else:
	cookie_window = ConfigCreator()
	cookie_window.set_main_window(voting_window)

	cookie_window.show()

sys.exit(app.exec_())
