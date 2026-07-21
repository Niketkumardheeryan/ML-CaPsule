import os

def rename_with_underscores(directory="."):
    """
    Recursively finds all files in the given directory and 
    replaces spaces in their filenames with underscores.
    """
    rename_count = 0
    
    # os.walk goes through all subdirectories and files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if " " in filename:
                # Generate the new name with underscores
                new_name = filename.replace(" ", "_")
                
                # Get the absolute paths for renaming
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_name)
                
                # Perform the rename
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: '{filename}'  ->  '{new_name}'")
                rename_count += 1
                
    print(f"\nTotal files renamed: {rename_count}")

if __name__ == "__main__":
    # You can change "." to a specific folder path if needed, e.g., "./dataset"
    print("Scanning directory for files with spaces...")
    rename_with_underscores(".")