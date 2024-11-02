
from pydantic import BaseModel, Field

class StartAnalysisInput(BaseModel):
    bucket_id: str = Field(...)