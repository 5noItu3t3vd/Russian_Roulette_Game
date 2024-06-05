import os
from config import *

def rename_files_to_png(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith('.png'):
                base = os.path.splitext(file)[0]
                new_name = f"{base}.png"
                os.rename(os.path.join(root, file), os.path.join(root, new_name))
    print(f"Succeeded! to print {directory}")

# Replace 'your_directory_path' with the path to the folder you want to process
rename_files_to_png(FAIL_OPP_SHOT)
