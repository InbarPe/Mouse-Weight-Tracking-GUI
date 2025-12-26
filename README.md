### Mouse Weight Tracking GUI

A GUI application for analyzing mouse weight in percentages over multiple experimental days. The program loads daily text files from a user-provided folder structure, extracts the animal’s weight from each file, and generates plots to visualize weight as a function of time. The tool also supports loading an external Python/MATLAB data file for comparison-based plotting.

## 📌 What Does This Project Do?

This project provides an easy interface to:

* Select a base path containing subfolders for each experimental day.

* Automatically load .txt files inside each folder and extract the mouse’s weight.

* Plot weight as a function of days.

* (Optional) Allow the user to drag and drop a Python or MATLAB file containing n values (where n = number of days) and generate a comparison plot of weight vs. those values.

* Display the plots inside the GUI with an option to save them as .png.

This tool is designed to help students and researchers quickly visualize behavioral experiment progress without manually handling files.

## 📁 Input Data Structure

The program expects a main folder containing one subfolder per experimental day:

BaseFolder/
    20251201/
        IP75_20251201_ExpDetails.txt
    20251202/
        IP75_20251202_ExpDetails.txt
    20251203/
        IP75_20251203_ExpDetails.txt
    ...

Subfolder Rules

Each subfolder name must be a date in the format:

YYYYMMDD  (YearMonthDay)


Example: 20251201

File Naming Rules

Each folder must contain exactly one .txt file that includes the text:

ExpDetails


Example:

IP75_20251201_ExpDetails.txt

# Optional Additional Input

If selected, the user can import a Python .py or MATLAB .m file containing a list/array of values such as:

# example_values.py
values = [10, 20, 30, 40, 50]


or

% example_values.m
values = [10, 20, 30, 40, 50];


These values will be used to generate a secondary plot:
mouse weight vs. file values.

## 🔍 Weight Extraction Rules

Inside each .txt file, the software will search for the mouse’s weight based on the following conditions:

Requirement	Must Appear On The Same Line
"BW"	✔ Yes
"%"	✔ Yes
A number before %	✔ This number is the weight value in percentages

Example valid line:

BW: 25.9g, 92%


Extracted value: 92

Invalid examples the program will ignore:
❌ % but no BW on the line
❌ BW present but no %
❌ No number before %

## 🖥️ GUI Features

* Text field to enter the base experiment folder path

* Button to scan folders and create Weight vs. Days plot

* Checkbox to enable external file loading

* Drag-and-drop input area for .py / .m files

* Separate button to generate the Weight vs. Custom Values plot

* Display plot in the application window

* Option to save plots as .png

## ⚙️ Technical Details
# Installation

Clone this repository:

git clone https://github.com/yourusername/Mouse-Weight-Tracking-GUI.git
cd Mouse-Weight-Tracking-GUI

# Dependencies

You can install the required packages using:

pip install -r requirements.txt


# Expected dependencies:

tkinter     # GUI
matplotlib  # plotting
numpy       # numeric handling
os/pathlib  # filesystem navigation

# Running the Application
python main.py

## 🧪 Testing

Tests will be included in a /tests folder.
Run them with:

pytest

## 📤 Output

* On-screen plot windows

* Option to save figures as .png

## 📚 Course Information

This project was created as a final assignment for the Python Programming Course (2025).
[Course repository link](https://github.com/Code-Maven/wis-python-course-2025-10)