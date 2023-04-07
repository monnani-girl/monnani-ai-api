from pydantic import BaseModel

class CropReqBody(BaseModel):
    season: str
    weather: str
    feel: str
    travel: str
    photo : str