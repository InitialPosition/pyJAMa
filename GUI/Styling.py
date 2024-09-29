from PySide6.QtWidgets import QMainWindow

from util import Config


def set_style(window: QMainWindow) -> None:
	"""
	Sets the style of the given window to the correct color scheme.
	:param window: The window to set the style for
	:return: None
	"""

	dark_mode_enabled = Config.load_config_key(Config.ConfigKeys.DARK_MODE.value)
	if dark_mode_enabled is None:
		dark_mode_enabled = True

	print(f"Dark mode is {dark_mode_enabled}")

	# set some colors based on the darkmode variable
	if dark_mode_enabled:
		col_background = "#161618"
		col_background_accent = "#252529"
		col_btn_enabled = "#050507"
		col_text = "#FFF"
		col_accent = "#404045"
		col_btn_disabled = "#101012"

	else:
		col_background = "#FFF"
		col_background_accent = "#AAA"
		col_btn_enabled = "#EEE"
		col_text = "#000"
		col_accent = "#252529"
		col_btn_disabled = "#666"

	window.setStyleSheet(f"""
			QMainWindow, QWidget {{
				background-color: {col_background};
			}}
			
			QMenu {{
				color: {col_text};
			}}
			
			QLineEdit {{
				text-color: {col_text};
				font-size: 12pt;
				background-color: {col_background_accent};
			}}
			
			QListWidget {{
				text-color: {col_text};
				font-size: 12pt;
				background-color: {col_background_accent};
			}}
			
			QPushButton {{
				background-color: {col_btn_enabled};
				border: 0px;
				font-size: 10pt;
				text-transform: uppercase;
				font-weight: bold;
				color: {col_text};
				padding: 10px;
			}}
			
			QPushButton:disabled {{
				background: {col_btn_disabled};
				color: {col_accent};
				border: 0px;
			}}
			
			QPushButton:checked {{
				background: {col_accent};
				border: 0px;
			}}
			
			QPushButton:hover {{
				background: {col_accent};
				border: 0px;
			}}
			
			QLabel {{
				color: {col_text};
			}}
	""")
