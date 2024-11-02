
from fastapi import status
from fastapi.routing import APIRouter

from model.start_analysis_input import StartAnalysisInput

namespace = APIRouter()


@namespace.post("/initiate",
                description="start analysis process",
                status_code=status.HTTP_200_OK)
def initiate_analysis(start_analysis_input: StartAnalysisInput):

    return "ok"


@namespace.get("/result/{process_id}",
                description="start analysis process",
                status_code=status.HTTP_200_OK)
def initiate_analysis(process_id: str):

    return "ok"
