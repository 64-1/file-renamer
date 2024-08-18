import os
import re

# List of file extensions to process
VALID_EXTENSIONS = [".csv", ".tif", ".sur"]

# Extract the first sequence of digits found in a given filename and return it as an integer
def extract_number(filename):
    number = re.search(r'(\d+)', filename)
    return int(number.group(0)) if number else None

def renaming(folder_path, file_extension):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
        
        # Handle .sur files specifically
        if file_extension == ".sur":
            handle_sur_files(folder_path, files)
            return

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
        
    except FileNotFoundError:
        print(f"Error: {folder_path} does not exist")
    except Exception as e:
        print(f"An error has occurred: {e}")

def handle_sur_files(folder_path, files):
    if len(files) == 1:
        print("Only one .sur file found. Skipping renaming.")
        return

    # Check for different naming formats
    filename_patterns = [extract_number(f) is not None for f in files]
    if len(set(filename_patterns)) > 1:
        print("Different naming formats detected in .sur files. Skipping renaming.")
        return

    # Proceed with renaming if all .sur files have the same format
    numbers = [(fname, extract_number(fname)) for fname in files]
    sorted_files = sorted([item for item in numbers if item[1] is not None], key=lambda x: x[1])
    renaming_rules = {old_name: f"{i + 1}.sur" for i, (old_name, _) in enumerate(sorted_files)}

    for old_name, new_name in renaming_rules.items():
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f'Renamed: "{old_path}" to "{new_path}"')

def rename_files_by_model(folder_path):
    model_map = {
        'a': [25, 50, 75, 100, 125, 150, 183, 200, 220, 240, 250, 260, 250, 240, 220, 200, 183, 150, 125, 100, 75, 50, 25],
        'b': [25, 50, 100, 150, 180, 150, 100, 50, 25],
        'c': [25, 50, 75, 100, 125, 100, 75, 50, 25]
    }

    while True:
        user_input = input('Please choose the model for renaming: 260C[a], 180C[b], 125C[c]\n').strip().lower()

        if user_input in model_map:
            for file_extension in VALID_EXTENSIONS:
                renaming(folder_path, file_extension)
                if file_extension != ".sur":
                    rename_files(folder_path, model_map[user_input], file_extension)
            print("Renaming completed successfully.")
            break
        else:
            print("Invalid input, please choose a valid model.")

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

def get_parent_directory(directory):
    return os.path.dirname(directory)

if __name__ == "__main__":
    folder_path = os.getcwd()
    parent_folder_path = get_parent_directory(folder_path)
    rename_files_by_model(parent_folder_path)
