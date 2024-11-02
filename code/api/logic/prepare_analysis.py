
import os
from fastapi import UploadFile
import shutil


data_folder_path = './data'

def create_process_directory(process_id: str):
    process_folder = f"{data_folder_path}/{process_id}" 
    print(process_folder)
    os.makedirs(process_folder, exist_ok=True)

def add_image_to_process_directory(process_id: str, file: UploadFile):

    process_folder = f"{data_folder_path}/{process_id}" 

    os.makedirs(process_folder, exist_ok=True)
    
    # Define the full path for the new file
    file_path = os.path.join(process_folder, file.filename)

    try:
        # Open the target file path within the process folder and copy the contents
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    return {"message": f"File {file.filename} uploaded successfully to {process_folder}"}