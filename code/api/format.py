# !pip install openai
# !pip install dspy
import ast
import asyncio
import enum
import json
import os
import sys
from typing import List, Literal

import dspy
import instructor
import numpy as np
import pandas as pd
from openai import OpenAI
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    confloat,
    model_validator,
)
from tqdm import tqdm

class ImageAnalyzer(BaseModel):
    description: str = Field(description="Long-form description of visible objects and what the user is doing.")
