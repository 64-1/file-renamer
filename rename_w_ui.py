import os
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QComboBox, QVBoxLayout, QWidget

VALID_EXTENSIONS = [".csv", ".tif", ".sur"]

# Extract number sequence from the files and return it 
def extract_number(filename):
    number = re.search(r'(\d+)', filename)
    return int(number.group(0)) if number else None

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def handle_tif_files(folder_path, files):
    #creates new folder path
    acq_folder = os.path.join(folder_path, "acq")
    comp_folders = {}

    for file in files:
        if file.startswith("acq"):
            create_folder_if_not_exists(acq_folder)
            os.rename(os.path.join(folder_path, file), os.path.join(acq_folder, file))
        elif file.startswith("comp"):
            # find all files that name starts wit comp + digit
            match = re.search(r'comp(\d+)', file)    
            if match:
                comp_number = match.group(1)
                comp_folder = os.path.join(folder_path, f"comp{comp_number}")
                if comp_number not in comp_folders:
                    create_folder_if_not_exists(comp_folder)
                    comp_folders[comp_number] = comp_folder
                os.rename(os.path.join(folder_path, file), os.path.join(comp_folder, file))

    # Rename files in the created folders
    for comp_folder in comp_folders.values():
        renaming_files_in_folder(comp_folder, ".tif")
    renaming_files_in_folder(acq_folder, ".tif")

def handle_sur_files(folder_path, files):
    sur_folder = None

    for file in files:
        if file.startswith("comp"):
            print("Comp sur found. Skipping renaming.")
            continue  # Skip to the next file
        elif file.startswith("acq"):
            if sur_folder is None:
                sur_folder = os.path.join(folder_path, "sur")
                create_folder_if_not_exists(sur_folder)
            os.rename(os.path.join(folder_path, file), os.path.join(sur_folder, file))

    if sur_folder is not None:
        renaming_files_in_folder(sur_folder, ".sur")

def handle_csv_files(folder_path, files):
    csv_folder = os.path.join(folder_path, "csv")
    create_folder_if_not_exists(csv_folder)

    for file in files:
        os.rename(os.path.join(folder_path, file), os.path.join(csv_folder, file))

    renaming_files_in_folder(csv_folder, ".csv")

def renaming_files_in_folder(folder_path, file_extension):
    if not os.path.exists(folder_path):
        print(f"Error: {folder_path} does not exist")
        return
    
    files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
    if not files:
        print(f"No files with extension {file_extension} found in {folder_path}.")
        return
    
    numbers = [(fname, extract_number(fname)) for fname in files]
    sorted_files = sorted([item for item in numbers if item[1] is not None], key=lambda x: x[1])
    renaming_rules = {old_name: f"{i + 1}{file_extension}" for i, (old_name, _) in enumerate(sorted_files)}

    for old_name, new_name in renaming_rules.items():
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f'Renamed: "{old_path}" to "{new_path}"')

def renaming(folder_path):
    for file_extension in VALID_EXTENSIONS:
        files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
        if file_extension == ".sur":
            handle_sur_files(folder_path, files)
        elif file_extension == ".csv":
            handle_csv_files(folder_path, files)
        elif file_extension == ".tif":
            handle_tif_files(folder_path, files)


def rename_files_by_model(folder_path, model):
    model_map = {
        'a': [25, 50, 75, 100, 125, 150, 183, 200, 220, 240, 250, 260, 250, 240, 220, 200, 183, 150, 125, 100, 75, 50, 25],
        'b': [25, 50, 100, 150, 180, 150, 100, 50, 25],
        'c': [25, 50, 75, 100, 125, 100, 75, 50, 25]
    }

    renaming(folder_path)

    for file_extension in VALID_EXTENSIONS:
        files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
        if file_extension != ".sur":
            rename_files(folder_path, model_map[model], file_extension)
    print("Renaming completed successfully.")

def rename_files(folder_path, numbers, file_extension):
    try:
        for i, number in enumerate(numbers):
            prefix = '0' if i == 0 or numbers[i] >= numbers[i - 1] else '1'
            old_filename = f"{i + 1}{file_extension}"
            new_filename = f"{prefix}_{number}{file_extension}"
            old_filepath = os.path.join(folder_path, old_filename)
            new_filepath = os.path.join(folder_path, new_filename)

            if os.path.exists(old_filepath):
                os.rename(old_filepath, new_filepath)
                print(f'Renamed: "{old_filename}" to "{new_filename}"')
            else:
                print(f"File: \"{old_filename}\" not found, skipping.")
    except Exception as e:
        print(f"An error occurred while renaming files: {e}")

class RenamingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Renaming Tool")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Select a folder and renaming model", self)
        layout.addWidget(self.label)

        # Folder selection button
        self.folder_button = QPushButton("Select Folder", self)
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_button)

        # Dropdown for selecting model
        self.model_dropdown = QComboBox(self)
        self.model_dropdown.addItems(["260C[a]", "180C[b]", "125C[c]"])
        layout.addWidget(self.model_dropdown)

        # Start renaming button
        self.rename_button = QPushButton("Start Renaming", self)
        self.rename_button.clicked.connect(self.start_renaming)
        layout.addWidget(self.rename_button)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.label.setText(f"Selected Folder: {self.folder_path}")

    def start_renaming(self):
        if not hasattr(self, 'folder_path'):
            self.label.setText("Please select a folder first.")
            return
        
        model_map = {
            "260C[a]": "a",
            "180C[b]": "b",
            "125C[c]": "c"
        }
        selected_model = self.model_dropdown.currentText()
        model_key = model_map[selected_model]
        
        rename_files_by_model(self.folder_path, model_key)
        self.label.setText("Renaming completed.")

if __name__ == "__main__":
    app = QApplication([])
    window = RenamingApp()
    window.show()
    app.exec_()
            
