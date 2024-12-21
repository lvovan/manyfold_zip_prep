import os
import shutil
import sys
from zipfile import ZipFile
import argparse

# Takes as a parameter a folder that contains the zip files to process
def process_zip_files(folder, output_folder, exclusion_list):
    # List all files in the folder
    files = os.listdir(folder)
    # Iterate over all files
    for file in files:
        print(f"Processing ZIP file {file}...")
        # Check if the file is a zip file
        if file.endswith('.zip'):
            # Open the zip file
            with ZipFile(os.path.join(folder, file), 'r') as zip_ref:
                # Find all folders in the zip file that only contain files and not other folders
                all_folders = [f for f in zip_ref.namelist() if f.endswith('/')]
                leaf_folders = []
                # sort alphabetically
                all_folders.sort()
                
                # If no folders, just copy the ZIP file to output_folder
                if len(all_folders) == 0:
                    shutil.copy2(os.path.join(folder, file), output_folder)
                    continue

                for i in range(len(all_folders)):
                    # Get the folder name
                    folder_name = all_folders[i]
                    # Get the files in the folder
                    files_in_folder = [f for f in zip_ref.namelist() if f.startswith(folder_name)]
                    if len(files_in_folder) > 1:
                        files_in_folder = files_in_folder[1:]
                    if not any(f.endswith('/') for f in files_in_folder):
                        is_excluded = False
                        for exclusion in exclusion_list:
                            if exclusion in folder_name:
                                is_excluded = True

                        if not is_excluded:
                            leaf_folders.append(folder_name)

                renamed_leaf_folders = []
                for lf in leaf_folders:
                    # Extract the folder
                    renamed_leaf_folders.append([lf, lf.replace(' ', '_').replace('/', '_')[:-1]])
                # for rf in renamed_leaf_folders:
                #     print(f" - '{rf[0]}' => '{rf[1]}'")

                # Now that we have the list of folders to extract, we can extract them 
                name_list = [name for name in zip_ref.namelist() if not name.endswith('/')]
                for rf in renamed_leaf_folders:
                    child_output_folder = os.path.join(output_folder, rf[1])
                    os.makedirs(child_output_folder, exist_ok=True)
                    for name in name_list:
                        if name.startswith(rf[0]):
                            new_name = name
                            if 'no_base' in new_name or 'No_Base' in new_name:
                                continue
                            elif '_base' in new_name or '_Base' in new_name:
                                new_name = new_name.replace('_base', '').replace('_Base', '')
                                # find the last occurence of "/" and replace it with "/zBase_"
                                last_slash = new_name.rfind('/')
                                new_name = new_name[:last_slash] + '/zBase_' + new_name[last_slash + 1:]
                            destination_path = os.path.join(child_output_folder, os.path.basename(new_name))
                            with zip_ref.open(name) as source, open(destination_path, 'wb') as target:
                                shutil.copyfileobj(source, target)

                    # Zip the new folder
                    with ZipFile(f"{child_output_folder}.zip", 'w') as zipf:
                        for root, _, files in os.walk(child_output_folder):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, child_output_folder)
                                zipf.write(file_path, arcname)

                    # Remove the folder
                    shutil.rmtree(child_output_folder)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process zip files in a folder.')
    parser.add_argument('folder', type=str, help='The folder containing zip files to process')
    parser.add_argument('output_folder', type=str, help='The folder to output the processed files')
    parser.add_argument('--exclusion_list', type=str, help='A list of strings to exclude from processing, in Python list format', default="['75mm', 'Supported', 'CHITUBOX']")
    return parser.parse_args()

args = parse_arguments()
folder = args.folder
output_folder = args.output_folder
exclusion_list = eval(args.exclusion_list)

# create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
process_zip_files(folder, output_folder, exclusion_list)