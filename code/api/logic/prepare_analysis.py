
import os

''' def prepare_analysis(bucket_id: str):
    data_folder_path = './data'
    process_folder = f"{data_folder_path}/{bucket_id}" 
    print(process_folder)
    os.makedirs(process_folder, exist_ok=True) '''


def create_process_directory(process_id: str):
    data_folder_path = './data'
    process_folder = f"{data_folder_path}/{process_id}" 
    print(process_folder)
    os.makedirs(process_folder, exist_ok=True)