import tkinter as tk
import numpy as np
from tkinter import filedialog, messagebox
from scipy.io import savemat
from datetime import datetime
from PIL import Image, ImageTk
from data_loader import find_day_folders, load_weights_for_selected_days
from external_values import load_single_values_file, load_daily_values_files
from plotter import plot_weights_vs_days, plot_weight_vs_external

class MouseWeightGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Weight Tracker")
        self.root.geometry("800x700")
        
        # Color scheme
        self.bg_color = "#313e4b"      # Dark blue-gray
        self.fg_color = "#ecf0f1"      # Light text
        self.accent_color = "#563d5f"  # Blue
        self.button_hover = "#1a2933"  # Darker blue
        
        # Apply colors to root
        self.root.configure(bg=self.bg_color)

        # Set window icon (QIcon equivalent)
        icon_img = Image.open("assets/logo.png")
        self.icon = ImageTk.PhotoImage(icon_img)
        self.root.iconphoto(True, self.icon)

        self.base_path = tk.StringVar()
        self.selected_days = []
        self.use_external = tk.BooleanVar()
        self.external_mode = tk.StringVar(value="single")
        self.single_values_file = tk.StringVar()

        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_main_gui()

    def _build_main_gui(self):
        # Top frame for instructions button
        top_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        top_frame.pack(fill="x", pady=(0, 10))
        
        tk.Button(
            top_frame,
            text="Instructions",
            command=self.show_instructions,
            bg=self.accent_color,
            fg="white",
            activebackground=self.button_hover,
            font=("Segoe UI", 9),
            padx=10,
            pady=5
        ).pack(side="right")
        
        tk.Label(self.main_frame, text="Base Folder", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 11, "bold")).pack(anchor="center", pady=(10, 5))
        tk.Entry(self.main_frame, textvariable=self.base_path, width=50, bg="#34495e", fg=self.fg_color, insertbackground=self.fg_color).pack(pady=5)
        tk.Button(self.main_frame, text="Browse", command=self.browse_folder, bg=self.accent_color, fg="white", activebackground=self.button_hover, font=("Segoe UI", 10)).pack(pady=5)

        tk.Button(self.main_frame, text="Load Days", command=self.load_days, bg=self.accent_color, fg="white", activebackground=self.button_hover, font=("Segoe UI", 10)).pack(pady=10)

        self.selected_days_label = tk.Label(
            self.main_frame,
            text="No days selected",
            bg=self.bg_color,
            fg="#95a5a6",
            font=("Segoe UI", 10)
        )
        self.selected_days_label.pack(anchor="center", pady=5)

        tk.Button(
            self.main_frame,
            text="Plot weight vs days",
            command=self.plot_weight_only,
            bg=self.accent_color,
            fg="white",
            activebackground=self.button_hover,
            font=("Segoe UI", 10)
        ).pack(pady=10)

        # Save format selection and button
        save_format_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        save_format_frame.pack(anchor="center", pady=(0, 10))
        
        tk.Label(
            save_format_frame,
            text="Save format:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(0, 5))

        self.save_format = tk.StringVar(value="mat")

        format_menu = tk.OptionMenu(
            save_format_frame,
            self.save_format,
            "mat",
            "npy"
        )
        format_menu.config(
            bg=self.accent_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            font=("Segoe UI", 10),
            highlightthickness=0
        )
        format_menu.pack(side="left", padx=(0, 10))

        tk.Button(
            save_format_frame,
            text="Save weights",
            command=self.save_selected_weights,
            bg=self.accent_color,
            fg="white",
            activebackground=self.button_hover,
            font=("Segoe UI", 10)
        ).pack(side="left")

        # External data checkbox
        tk.Checkbutton(
            self.main_frame,
            text="Add external daily values",
            variable=self.use_external,
            command=self.toggle_external_options,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.accent_color,
            font=("Segoe UI", 10)
        ).pack(anchor="center", pady=(15, 5))

        # Container for ALL external-related UI
        self.external_container = tk.Frame(self.main_frame, bg=self.bg_color)

        # ---- External options ----
        self.external_frame = tk.Frame(self.external_container, bg=self.bg_color)

        tk.Radiobutton(
            self.external_frame,
            text="One file with all values",
            variable=self.external_mode,
            value="single",
            command=self.update_external_ui,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.accent_color,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Radiobutton(
            self.external_frame,
            text="One file per day",
            variable=self.external_mode,
            value="daily",
            command=self.update_external_ui,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.accent_color,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        # ---- Single file UI ----
        self.single_file_frame = tk.Frame(self.external_frame, bg=self.bg_color)

        tk.Label(self.single_file_frame, text="Values file:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 10)).pack(side="left")
        tk.Entry(
            self.single_file_frame,
            textvariable=self.single_values_file,
            width=40,
            # state="readonly",
            bg="#34495e",
            fg=self.fg_color,
            insertbackground=self.fg_color
        ).pack(side="left", padx=5)

        tk.Button(
            self.single_file_frame,
            text="Browse",
            command=self.browse_single_values_file,
            bg=self.accent_color,
            fg="white",
            activebackground=self.button_hover,
            font=("Segoe UI", 9)
        ).pack(side="left")

        # ---- Daily file UI ----
        self.daily_filename_frame = tk.Frame(self.external_frame, bg=self.bg_color)

        tk.Label(self.daily_filename_frame, text="Daily filename:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 10)).pack(side="left")
        self.external_filename_entry = tk.Entry(
            self.daily_filename_frame,
            width=30,
            bg="#34495e",
            fg="#95a5a6",
            insertbackground=self.fg_color,
            font=("Segoe UI", 10)
        )

        self.daily_placeholder = "example: daily_value.npy"
        self.external_filename_entry.insert(0, self.daily_placeholder)
        self.external_filename_entry.pack(side="left")

        self.external_filename_entry.bind("<FocusIn>", self._clear_placeholder)
        self.external_filename_entry.bind("<FocusOut>", self._restore_placeholder)

        self.show_regression = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.external_frame,
            text="Show linear regression",
            variable=self.show_regression,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.accent_color,
            font=("Segoe UI", 10),
            activebackground=self.bg_color,
            activeforeground=self.fg_color
        ).pack(anchor="w", pady=(10, 0))

        self.mark_outliers = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.external_frame,
            text="Mark outliers (z-score)",
            variable=self.mark_outliers,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.accent_color,
            font=("Segoe UI", 10),
            activebackground=self.bg_color,
            activeforeground=self.fg_color
        ).pack(anchor="w", pady=(10, 0))

        self.outlier_thresh = tk.DoubleVar(value=3.0)
        thresh_frame = tk.Frame(self.external_frame, bg=self.bg_color)
        thresh_frame.pack(anchor="w", pady=(5, 0))
        
        tk.Label(
            thresh_frame,
            text="Outlier threshold:",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(0, 5))

        tk.Spinbox(
            thresh_frame,
            from_=0.5,
            to=10.0,
            increment=0.1,
            width=5,
            textvariable=self.outlier_thresh,
            bg="#34495e",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        ).pack(side="left", padx=5)

        # ---- Plot external button (IMPORTANT: packed LAST) ----
        self.plot_external_button = tk.Button(
            self.external_container,
            text="Plot weight vs external values",
            command=self.plot_with_external,
            bg=self.accent_color,
            fg="white",
            activebackground=self.button_hover,
            font=("Segoe UI", 10)
        )

    def _clear_placeholder(self, event):
        if self.external_filename_entry.get() == self.daily_placeholder:
            self.external_filename_entry.delete(0, "end")
            self.external_filename_entry.config(fg="black")

    def _restore_placeholder(self, event):
        if not self.external_filename_entry.get().strip():
            self.external_filename_entry.insert(0, self.daily_placeholder)
            self.external_filename_entry.config(fg="gray")


    def browse_single_values_file(self):
        file = filedialog.askopenfilename(
        title="Select values file",
        filetypes=[
            ("NumPy files", "*.npy"),
            ("Pickle files", "*.pkl"),
            ("MATLAB files", "*.mat")
        ]
    )

        if file:
            self.single_values_file.set(file)

    def update_external_ui(self):
        self.single_file_frame.pack_forget()
        self.daily_filename_frame.pack_forget()

        if self.external_mode.get() == "single":
            self.single_file_frame.pack(anchor="w", pady=3)
        elif self.external_mode.get() == "daily":
            self.daily_filename_frame.pack(anchor="w", pady=3)


    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.base_path.set(path)

    def toggle_external_options(self):
        if self.use_external.get():
            self.external_container.pack(anchor="center", pady=5)
            self.external_frame.pack(anchor="w")
            self.update_external_ui()
            self.plot_external_button.pack(anchor="w", pady=(5, 0))
        else:
            self.external_container.pack_forget()


    def plot_weight_only(self):
        if not self.ensure_days_loaded():
            return
        self.process_data()

    def plot_with_external(self):
        if not self.selected_days:
            messagebox.showerror(
                "No days selected",
                "Please load and confirm days to process."
            )
            return

        mode = self.external_mode.get()

        try:
            if mode == "single":
                values = load_single_values_file(
                    self.single_values_file.get()
                )

            elif mode == "daily":
                filename = self.external_filename_entry.get().strip()

                if (
                    not filename
                    or filename == self.daily_placeholder
                ):
                    messagebox.showerror(
                        "Missing input",
                        "Please enter a daily external data filename."
                    )
                    return

                values = load_daily_values_files(
                    self.selected_days,
                    filename
                )

            else:
                raise RuntimeError("Unknown external data mode")

            weights = load_weights_for_selected_days(self.selected_days)
            plot_weight_vs_external(weights, values, show_regression=self.show_regression.get(), mark_outliers=self.mark_outliers.get(), z_thresh=self.outlier_thresh.get())

        except Exception as e:
            messagebox.showerror("Error", str(e))



    def load_days(self):
        base_path = self.base_path.get()
        if not base_path:
            messagebox.showerror("Error", "Please select a base folder first.")
            return

        try:
            self.day_folders = find_day_folders(base_path)
            self.open_day_selector()
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def ensure_days_loaded(self):
        if not self.selected_days:
            messagebox.showerror(
                "Error",
                "No days loaded.\nPlease click 'Load days' and select days first."
            )
            return False
        return True


    def open_day_selector(self):
        popup = tk.Toplevel(self.root)
        popup.title("Select Days to Process")
        popup.geometry("350x400")
        popup.configure(bg=self.bg_color)
        
        # Scrollable frame for checkboxes
        canvas_frame = tk.Frame(popup, bg=self.bg_color)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg=self.bg_color, highlightthickness=0, height=250)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.day_vars = {}
        for folder in self.day_folders:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(
                scrollable_frame,
                text=folder.name,
                variable=var,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor=self.accent_color,
                font=("Segoe UI", 11),
                activebackground=self.bg_color,
                activeforeground=self.fg_color
            )
            cb.pack(anchor="w", pady=5)
            self.day_vars[folder] = var
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ok_button = tk.Button(
            popup,
            text="OK",
            command=lambda: self.confirm_day_selection(popup),
            bg=self.accent_color,
            fg="white",
            activebackground=self.button_hover,
            font=("Segoe UI", 10),
            padx=20,
            pady=8
        )
        ok_button.pack(pady=10)


    def confirm_day_selection(self, popup):
        popup.destroy()

        self.selected_days = [d for d, v in self.day_vars.items() if v.get()]
        if not self.selected_days:
            messagebox.showerror("Error", "No days selected.")
            self.selected_days = []
            self.selected_days_label.config(text="No days selected", fg="gray")
            return

        dates = [d.name for d in self.selected_days]
        self.selected_days_label.config(
            text="Selected days: " + ", ".join(dates),
            fg="black"
        )


    def process_days(self, popup):
        popup.destroy()
        self.plot_weight_only()


    def process_data(self):
        selected_days = self.selected_days
        dates = [d.name for d in selected_days]


        if not selected_days:
            messagebox.showerror("Error", "No days selected")
            return

        try:
            weights = load_weights_for_selected_days(self.selected_days)

            plot_weights_vs_days(weights, dates=dates)

        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def show_instructions(self):
        win = tk.Toplevel(self.root)
        win.title("Information")
        win.geometry("600x500")
        win.configure(bg=self.bg_color)

        text = tk.Text(
            win,
            wrap="word",
            padx=10,
            pady=10,
            bg="#34495e",
            fg=self.fg_color,
            font=("Segoe UI", 10),
            insertbackground=self.fg_color,
            highlightbackground=self.accent_color,
            highlightcolor=self.accent_color
        )
        text.pack(fill="both", expand=True)

        instructions = """
    FOLDER STRUCTURE
    ------------------------
    The program expects a main folder containing subfolders for each experimental day:

    BaseFolder/
        20251201/
            IP75_20251201_ExpDetails.txt
        20251202/
            IP75_20251202_ExpDetails.txt
        ...

    • Subfolder names must be dates in YYYYMMDD format
    • Each subfolder must contain exactly one *.txt file that its name include 'ExpDetails'


    WEIGHT EXTRACTION RULES
    ----------------------------------
    • The weight must appear in a line that includes:
        - 'BW'
        - '%'
    • The program extracts the numeric value before '%'
    • Decimal values are supported

    Examples:
        BW: 83% 21.2g
        BW: 81.5% 20.8g


    EXTERNAL DATA OPTIONS
    -------------------------------
    Option 1: One file with all values
    • Provide a .npy / .pkl / .mat file
    • Number of values must match number of selected days

    Option 2: One file per day
    • Provide a filename (e.g. daily_values.npy)
    • File must exist in each selected day folder
    • Each file must contain a single numeric value


    OUTLIERS DETECTION
    --------------------------
    • When enabled, outliers in weight data are marked on the plot
    • Outliers are detected using z-score method
    • Adjust the threshold as needed (default is 3.0)
    • Threshold is the number of standard deviations from the mean that defines an outlier
    • Higher threshold = fewer outliers detected
    """

        text.insert("1.0", instructions)
        text.config(state="disabled")


    def save_selected_weights(self):
        """Save extracted weights if days are selected."""
        if not self.selected_days:
            messagebox.showerror("Error", "Please load and select days first.")
            return
        
        try:
            weights = load_weights_for_selected_days(self.selected_days)
            self.save_extracted_weights(weights, self.selected_days)
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def save_extracted_weights(self, weights, selected_days):
        """Save extracted weights in the selected format."""
        
        save_format = self.save_format.get()
        
        # Create a default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"weights_{timestamp}"

        # Create data to save
        dates = [d.name for d in selected_days]
        data = {"weights": weights, "dates": np.array(dates, dtype=object)}
        
        try:
            if save_format == "mat":
                # Save as MATLAB file
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".mat",
                    initialfile=default_filename + ".mat",
                    filetypes=[("MATLAB files", "*.mat"), ("All files", "*.*")]
                )
                if file_path:
                    savemat(file_path, data)
                    messagebox.showinfo("Success", f"Weights saved to:\n{file_path}")
                    
            elif save_format == "npy":
                # Save as NumPy file
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".npy",
                    initialfile=default_filename + ".npy",
                    filetypes=[("NumPy files", "*.npy"), ("All files", "*.*")]
                )
                if file_path:
                    np.save(file_path, data)
                    messagebox.showinfo("Success", f"Weights saved to:\n{file_path}")
                    
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save weights:\n{str(e)}")
