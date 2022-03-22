import os
from argparse import ArgumentParser
from json import dumps, loads
from os.path import abspath, getmtime, isfile


# function to clear terminal
def clear_terminal():
	os.system('cls' if os.name == 'nt' else 'clear')


def print_logo():
	logo_file = "logo.txt"
	with open(logo_file, "r") as f:
		logo = f.read()
		print(logo)


def get_all_ui_files(path):
	ui_files_ = []
	for root, dirs, files in os.walk(path):
		for file_ in files:
			if file_.endswith(".ui"):
				ui_files_.append(os.path.join(file_))
	return ui_files_


def get_last_modified_dates():
	try:
		with open("compile_times", "r") as f:
			data = f.read()

		modify_dates_ = loads(data)

	except FileNotFoundError:
		print("No saved compile times found")
		return {}

	return modify_dates_


def save_last_modified_dates():
	for file_ in ui_files:
		modified_at = getmtime(file_)
		modify_dates.update({file_: modified_at})

	with open("compile_times", "w") as f:
		f.write(dumps(modify_dates))
		f.write("\n")


# set force compile flag
parser = ArgumentParser()
parser.add_argument(
	"-f", "--force", action="store_true", help="Compile all found ui files independent of their last "
	                                           "compile time"
)
parser.add_argument("-v", "--verbose", action="store_true", help="Output more info during conversion")
args = parser.parse_args()

# load dates if they exist
modify_dates = get_last_modified_dates()

clear_terminal()
print_logo()
print("v1.1\n")

# find all ui files in designer folder
work_path = os.getcwd()

if args.verbose:
	print(f"Search Path: {work_path}")

ui_files = get_all_ui_files(work_path)

print(f"{len(ui_files)} files found. Converting...\n")

# convert ui files to py files using pyside2-uic
if args.force:
	print("--- FORCE COMPILING ENABLED ---\n")

convert_count = 0
parent_directory = abspath(os.path.join(os.getcwd(), os.pardir))
for file in ui_files:
	if isfile(os.path.join(parent_directory, 'ui_' + file.replace('.ui', '.py'))):
		if file in modify_dates:
			if getmtime(file) <= modify_dates[file] and not args.force:
				if args.verbose:
					print(f"Skipping {file}, newest compiled ui already present")
				continue

	print(f"Converting {file} to .py file... ", end="")
	os.system(f"pyside2-uic {file} -o ui_{file.replace('.ui', '.py')}")
	os.system(f"mv ui_{file.replace('.ui', '.py')} {parent_directory}")  # TODO add flag to disable file moving

	convert_count += 1

	print("done.")

print("\nCompleted. ", end="")
if convert_count == 0:
	print("No UI files were compiled.\n")
elif convert_count == 1:
	print("1 UI file compiled.\n")
else:
	print(f"{convert_count} UI files compiled.\n")
save_last_modified_dates()
