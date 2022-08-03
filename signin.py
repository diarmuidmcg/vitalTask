from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
app = FastAPI()

    # to my understanding, this is the flow
    #   call the /{patientId}/export ENDPOINT
    #       -> that TAKES a Captcha parameter 
    #       * i need to figure out a way to get past this *
    #   the /export endpoint will a hub-eu endpoint
    #   call that hub-eu endpoint, it will return 2 links
    #       -> a wss that is a secure web portal (I don't think i need that)
    #       -> a link to their aws with the query parameters already filled in
    #   call that aws endpoint -> i'll get the data I need
    #       -> store that data in my sqlite database
    #   
    

# this takes in a type-glucose & captchaResponse & patientId
@app.post("/generate-data")
async def generate_data(type:str, captchaResponse: str, patientId: str):
    

    # AWAIT STEP 1
    # call the export endpoint to 
    # async with httpx.AsyncClient() as client:
    #     callback_url = "https://api-eu.libreview.io/patients/{patientId}/export"
    #     exportResponse = await client.post(callback_url, data={"type":type,"captchaResponse":captchaResponse})

    
    # AWAIT STEP 2
    # the export endpoint will return an endpoint that is hub-eu -> call that 
    # async with httpx.AsyncClient() as client:
    #     callback_url = exportResponse.url
    #     hubResponse = await client.get(callback_url})

    # AWAIT STEP 3
    # the export endpoint will return an an aws endpoint -> call that 
    # async with httpx.AsyncClient() as client:
    #     callback_url = hubResponse.ld
    #     awsResponse = await client.get(callback_url})
    
    #  the awsResponse will be a large batch of data 
    #  store this data in a sqlite database 
    
    


    return {"data": creds}
    
# ENDPOINT to generate a proper captchaResponse
# not entirely sure how to do that atm
    # send that code to the api
    # async with httpx.AsyncClient() as client:
    #     callback_url = "https://api-eu.libreview.io/auth/continue/2fa/result"
    #     response = await client.post(callback_url)
    #     print(response.json())
    
    # with this response, you should properly be able to get the user data
    
