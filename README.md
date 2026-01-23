# Mouse Weight Tracker GUI

A GUI application for analyzing mouse weight in percentages over multiple experimental days. The program loads daily text files from a user-provided folder structure, extracts the animal’s weight from each file, and generates plots to visualize weight as a function of time. The tool also supports loading an external Python/MATLAB data file for comparison-based plotting.

## 📌 What Does This Project Do?

This project provides an easy interface to:

* Select a base path containing subfolders for each experimental day.

* Automatically load .txt files inside each folder and extract the mouse’s weight.

* Plot weight as a function of days.

* Allow exporting all extracted weight measurements from the selected days. Users may save the data as either a MATLAB (.mat) or a Python (.npy) file.

* Allow the user to load a Python or MATLAB file containing n values (where n = number of days) and generate a comparison plot of weight vs. those values.

* Scatter plot for external values with:
  - Pearson correlation (r)
  - p-value
  - Optional linear regression overlay
  - Optional outlier marking

* Display the plots inside the GUI with an option to save them as .png.

* Clear error handling and user-friendly pop-up messages.

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

### Subfolder Rules

Each subfolder represents one experimental day and its name must be a date in the format:

YYYYMMDD  (YearMonthDay)


Example: 20251201

### File Naming Rules

* Each folder must contain exactly one .txt file that includes the text: ExpDetails
* Example: IP75_20251201_ExpDetails.txt

## Optional Additional Input

The user may optionally plot mouse weight against an external daily variable.
Two modes are supported:

### Option 1: One file with all values
- A single file containing one value per day
- Supported formats: `.npy`, `.mat`
- Number of values must match the number of selected days

Examples:

    # example_values.npy
    values = [10, 20, 30, 40, 50]


    or

    % example_values.m
    values = [10, 20, 30, 40, 50];

### Option 2: One file per day
- A file with the same name in each selected day folder
- Each file must contain **a single numeric value**
- Supported formats: `.npy`, `.mat`

File name and format examples: 
    - daily_value.py
    - daily_value.m

And the file will look like:

    # daily_value.npy
    value = 10


    or

    % daily_value.m
    value = 10;

All values from each day that was dselected to be processed will be combined to one list for the visualiztion.

These values will be used to generate a secondary plot:
mouse weight vs. file values.

## 🔍 Weight Extraction Rules

Inside each .txt file, the software will search for the mouse’s weight based on the following conditions:

! Requirement	Must Appear On The Same Line

✔ "BW"

✔ "%"

✔ A number before %	 (This number is the weight value in percentages)

Example valid line: BW: 25.9g, 92%

Extracted value: 92

Invalid examples the program will ignore:

❌ % but no BW on the line

❌ BW present but no %

❌ No number before %

## 📊 Statistical Analysis

When plotting weight vs external values:

- Data is shown as a **scatter plot**
- Pearson correlation coefficient (r) and p-value are displayed
- Optional linear regression overlay
- Optional outlier marking

### Outlier definition

Outliers are identified using a **z-score–based method**:

- A data point is considered an outlier if its weight or external value
  deviates by more than a specified number of standard deviations
  (default: 3) from the mean.
- The outlier detection threshold is user-configurable, allowing flexible control over sensitivity depending on dataset size and   variability.
- Outliers are **not removed**
- They are visually marked on the plot
- Correlation and regression are computed using inlier data only

This ensures transparency and preserves data integrity.

## ⚙️ Technical Details
### Installation

Clone this repository:

git clone https://github.com/InbarPe/Mouse-Weight-Tracking-GUI.git

cd Mouse-Weight-Tracking-GUI

### Dependencies

You can install the required packages using:

    pip install -r requirements.txt

### Running the Application
python main.py

## 🧪 Testing

The project includes automated tests for core logic (data loading, parsing, validation).
Tests are included in a /tests folder.
Run them with:

pytest -v

## 📤 Output

* On-screen plot windows

* Option to save figures as .png

## 📚 Course Information

This project was created as a final assignment for the Python Programming Course (2025).

[Course repository link](https://github.com/Code-Maven/wis-python-course-2025-10)

## 👤 Author

Inbar Perets Vadavker
