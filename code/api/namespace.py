
import os, uuid
from fastapi import status
from fastapi.routing import APIRouter
from logic.prepare_analysis import create_process_directory

import shutil

from model.start_analysis_input import StartAnalysisInput

from fastapi import FastAPI, File, UploadFile


namespace = APIRouter()


@namespace.post("/initiate-process",
                description="start analysis process",
                status_code=status.HTTP_200_OK)
def initiate_analysis(start_analysis_input: StartAnalysisInput):
    '''     prepare_analysis(start_analysis_input.bucket_id)'''    
    return "ok"


@namespace.get("/result/{process_id}",
                description="start analysis process",
                status_code=status.HTTP_200_OK)
def initiate_analysis(process_id: str):

    return "ok"

@namespace.post("/create-process",
    description="create process",
                status_code=status.HTTP_200_OK)
def create_process():
    process_id = str(uuid.uuid1())
    create_process_directory(process_id)
    return process_id


@namespace.post("/add_image/{process_id}",
    description="add image to process",
                status_code=status.HTTP_200_OK)
def add_image_to_process(process_id: str, file: UploadFile):
    data_folder_path = './data'
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