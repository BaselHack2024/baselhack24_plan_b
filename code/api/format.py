from typing import List
from pydantic import (BaseModel, Field, )


class ImageAnalyzer(BaseModel):
    description: str = Field(description="Long-form description of visible objects and what the user is doing.")


class Step(BaseModel):
    step: int = Field(description="Step number")
    instruction: str = Field(description="Instruction for the step")


class Guide(BaseModel):
    object: str = Field(description="Short name of the object")
    goal: str = Field(description="Long-form description of what the user is doing/assembling/operating")
    steps: List[Step] = Field(description="For each of the input images exactly one step")


# Subclass for exactly 3 steps
class ThreeStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 3 steps", min_length=3, max_length=3)


# Subclass for exactly 4 steps
class FourStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 4 steps", min_length=4, max_length=4)


# Subclass for exactly 5 steps
class FiveStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 5 steps", min_length=5, max_length=5)


# Subclass for exactly 6 steps
class SixStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 6 steps", min_length=6, max_length=6)


# Subclass for exactly 7 steps
class SevenStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 7 steps", min_length=7, max_length=7)


# Subclass for exactly 8 steps
class EightStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 8 steps", min_length=8, max_length=8)


# Subclass for exactly 9 steps
class NineStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 9 steps", min_length=9, max_length=9)


# Subclass for exactly 10 steps
class TenStepGuide(Guide):
    steps: List[Step] = Field(description="Guide with exactly 10 steps", min_length=10, max_length=10)


# Factory function to return the correct class based on expected_number
def get_guide_class(expected_number: int):
    if expected_number == 3:
        return ThreeStepGuide
    elif expected_number == 4:
        return FourStepGuide
    elif expected_number == 5:
        return FiveStepGuide
    elif expected_number == 6:
        return SixStepGuide
    elif expected_number == 7:
        return SevenStepGuide
    elif expected_number == 8:
        return EightStepGuide
    elif expected_number == 9:
        return NineStepGuide
    elif expected_number == 10:
        return TenStepGuide
    else:
        raise ValueError("Invalid expected number. Must be between 5 and 10.")
