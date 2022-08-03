from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import httpx


app = FastAPI()

bearerToken = ""


# main function that'll return all the data requested from the data pool
@app.get("/glucose")
async def get_glucose(start_date: str = "", end_date: str = ""):
    
    # ensure signed in 
        # if not, prompt user to call /signin endpoint
    
    # ensure params includes
    if not start_date or not end_date:
        return {"error": "You did not pass in the correct parameters"}
    # validate that the start date & end date are the proper YYYY-MM-DD format
    # and that they are all valid numbers / years
    
    
    # ensure the data has been loaded
        # if not, prompt user to call the /generate-data endpoint 
    
    
    # search data pool based on parameters passed in

    # sanitize the data & put in desired JSON object to return
    
    data = start_date + end_date
    return {"data": data}
