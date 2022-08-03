from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import httpx


app = FastAPI()

class SignInObject(BaseModel):
    email: str
    password: str

    
# sign in function that will pass take a username & password & send it to 
# LibreView
@app.post("/signin")
async def sign_in_user(creds: SignInObject):
    
    # AWAIT STEP 1
    # get the bearerToken by calling the config endpoint 
    # pass in the country GB
    # async with httpx.AsyncClient() as client:
    #     callback_url = "https://api-eu.libreview.io/config"
    #     response = await client.post(callback_url, data={"country":"GB"})
    #     print(response.json())
    
    # AWAIT STEP 2
    # sign in with the email, password, & bearerToken from the above endpoint
    async with httpx.AsyncClient() as client:
        callback_url = "https://api-eu.libreview.io/auth/signin"
        response = await client.post(callback_url, data={"email":creds.email, "password":creds.password, "fingerprint":"2,(Macintosh),Mozilla/(Macintosh;IntelMacOSX;rv:)Gecko/Firefox/,Intel(R)HDGraphics400,America/New_York,5,MacIntel,en-US,en-US,en,4,"})
        print(response.json())

    # IF the user is not remembered (needs confirmation token)
    
    # generate the access token to be sent to the email
    # async with httpx.AsyncClient() as client:
    #     callback_url = "https://api-eu.libreview.io/auth/continue/2fa/sendcode"
    #     response = await client.post(callback_url)
    #     print(response.json())
    
    # return here & tell the user to call the endpoint to send the code to libreview
    
    


    return {"data": creds}
    
# ENDPOINT to submit the confirmation code & get the bearerToken 
    # send that code to the api
    # async with httpx.AsyncClient() as client:
    #     callback_url = "https://api-eu.libreview.io/auth/continue/2fa/result"
    #     response = await client.post(callback_url)
    #     print(response.json())
    
    # with this response, you should properly be able to get the user data
    
