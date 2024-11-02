
from pydantic import BaseModel, Field

class StartAnalysisInput(BaseModel):
    process_id: str = Field(...)