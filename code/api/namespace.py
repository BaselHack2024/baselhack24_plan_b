
import uuid
from fastapi import status, BackgroundTasks
from fastapi.routing import APIRouter
from logic.run_analysis import run_process_analysis
from logic.prepare_analysis import add_image_to_process_directory, create_process_directory

from model.start_analysis_input import StartAnalysisInput

from fastapi import UploadFile

import os

namespace = APIRouter()


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
    return add_image_to_process_directory(process_id, file)


@namespace.post("/initiate-process",
                description="start analysis process",
                status_code=status.HTTP_200_OK)
async def initiate_analysis(start_analysis_input: StartAnalysisInput, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_process_analysis, start_analysis_input.process_id)
    return "ok"


@namespace.get("/result/{process_id}",
                description="check process",
                status_code=status.HTTP_200_OK)
def check_result(process_id: str):
    return os.path.exists(f"./data/{process_id}/result.json")
