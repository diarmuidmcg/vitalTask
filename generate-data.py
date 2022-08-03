from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
app = FastAPI()


# this takes in a type-glucose & captchaResponse & patientId
@app.post("/generate-data")
async def generate_data(type:str, captchaResponse: str, patientId: str):
    


    return {"data": creds}
