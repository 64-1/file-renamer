import os
import re

"""This is a file renaming script

This script renames files with certain formats namely .csv, .tif and .suf into desired names according to the temperature list.

"""

# Extract the first sequence of digits found in a given filename and returns it as an integer
def extract_number(filename):
    # Use the regular expression search to find the first sequence of of one or more digits in the file
    number = re.search(r'(\d+)', filename)
    if number:
        # Return the matched string after it is converted into integer
        return int(number.group(0))
    else:
        return None



def renaming(folder_path):
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    sur_files = [f for f in os.listdir(folder_path) if f.endswith('.sur')]
    tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]
    
    # Extract numbers from filenames
    numbers = [(fname, extract_number(fname)) for fname in csv_files]
    numbers_s = [(fname, extract_number(fname)) for fname in sur_files]
    numbers_t = [(fname, extract_number(fname)) for fname in tif_files]

    
    # Filter out files where no number was found and sort by the extracted number
    sorted_files = sorted([item for item in numbers if item[1] is not None], key=lambda x: x[1])
    
    # Create a mapping of old filenames to new filenames based on the sorted order
    renaming_rules = {old_name: f"{i+1}.csv" for i, (old_name, _) in enumerate(sorted_files)}
    
    # Rename files according to the mapping
    for old_name, new_name in renaming_rules.items():
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)

def rename_csv_files(folder_path):
    # Count the number of .csv files
    renaming(folder_path)

    user_input = input('Please choose the model for renaming: 260C[a], 180C[b], 125[C]\n')
    
    # Select renaming algorithm based on the number of files
    if user_input == 'a':
        renaming_rule = rename_rule_23
    elif user_input == 'b':
        renaming_rule = rename_rule_9A
    elif user_input == 'c':
        renaming_rule = rename_rule_9B
    else:
        print("Unusual input detected, exiting ")

    renaming_rule(folder_path)
    

def rename_rule_23(folder_path):
    numbers = [25, 50, 75, 100, 125, 150, 183, 200, 220, 240, 250, 260, 250, 240, 220, 200, 183, 150, 125, 100, 75, 50, 25]
    rename_files(folder_path, numbers)

def rename_rule_9A(folder_path):
    numbers = [25, 50, 100, 150, 180, 150, 100, 50, 25]
    rename_files(folder_path, numbers)

def rename_rule_9B(folder_path):
    numbers = [25, 50, 75, 100, 125, 100, 75, 50, 25]
    rename_files(folder_path, numbers)

def rename_files(folder_path, numbers):
    for i, number in enumerate(numbers):
        if i == 0 or numbers[i] >= numbers[i-1]:
            prefix = '0'
        else:
            prefix = '1'

        old_filename = f"{i+1}.csv"
        new_filename = f"{prefix}_{number}.csv"
        old_filepath = os.path.join(folder_path, old_filename)
        new_filepath = os.path.join(folder_path, new_filename)

        os.rename(old_filepath, new_filepath)
        print(f'Renamed:{old_filename} to {new_filename}')
    
def get_parent_directory(directory):
    return os.path.dirname(directory)

if __name__ == "__main__":
    # Get the current file path
    folder_path = os.getcwd()
    parent_folder_path = get_parent_directory(folder_path)
    rename_csv_files(parent_folder_path)