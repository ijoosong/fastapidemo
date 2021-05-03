from pydantic import BaseModel


class PartOption(BaseModel):
    """Valid options for a griffy avatar component."""

    r: int
    g: int
    b: int


class Colour(BaseModel):
    """Valid options for a griff-ify colors."""

    base: PartOption
    circle: PartOption
