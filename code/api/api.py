"""This is the api module."""

from fastapi import APIRouter, FastAPI
from namespace import namespace

def init_api(app: FastAPI):
    """Initialize fast api app.

    This function initializes a fast api app
    and adds to it all necessary routes.

    Args:
        app : FastAPI
            An instance of a fast api app
    """
    # Include API router in fast api app instance
    app.include_router(api_v1)


@api_v1.post("/create-process",
    description="create process",
                status_code=status.HTTP_200_OK)
def create_process():
    process_id = str(uuid.uuid1())
    create_process_directory(process_id)
    return process_id


@api_v1.post("/add_image/{process_id}",
    description="add image to process",
                status_code=status.HTTP_200_OK)
def add_image_to_process(process_id: str, file: UploadFile):
    return add_image_to_process_directory(process_id, file)


@api_v1.post("/initiate-process",
                description="start analysis process",
                status_code=status.HTTP_200_OK)
async def initiate_analysis(start_analysis_input: StartAnalysisInput, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_process_analysis, start_analysis_input.process_id)
    return "ok"


@api_v1.get("/result/{process_id}",
                description="check process",
                status_code=status.HTTP_200_OK)
def check_result(process_id: str):
    return os.path.exists(f"./data/{process_id}/result.json")



