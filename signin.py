from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import httpx


# "authTicket": {
#     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQzZGQ5NGM2LWZjMWUtMTFlYi1iYTIzLTAyNDJhYzExMDAwNCIsImZpcnN0TmFtZSI6InRhc2siLCJsYXN0TmFtZSI6InRyeXZ0YWlsIiwiY291bnRyeSI6IkdCIiwicmVnaW9uIjoiZXUiLCJyb2xlIjoiaGNwIiwiZW1haWwiOiJ0YXNrQHRyeXZpdGFsLmlvIiwiYyI6MSwicyI6Imx2IiwiZXhwIjoxNjU5NTU4ODE2fQ.s9gpq93xiJBhVIIjRuz__RaeGvSJCD2b7-BbITTP_T4",
#     "expires": 1659558816,
#     "duration": 3600000
# }


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
        callback_url = "https://api-eu.libreview.io/auth/login"
        loginResponse = await client.post(callback_url, data={"email":creds.email, "password":creds.password})
        bearerToken = loginResponse.data.authTicket
        verify = loginResponse.step
        # print(response.json())

    # IF the user is not remembered (needs confirmation token)
    
    #  if verify.type == "2faVerify"
    # email is verify.props.secondaryValue
    
    # generate the access token to be sent to the email
    # async with httpx.AsyncClient() as client:
    #     callback_url = "https://api-eu.libreview.io/auth/continue/2fa/sendcode"
    #     sendCodeResponse = await client.post(callback_url)
    #     # this generates a NEW bearerToken as well
    #     bearerToken = sendCodeResponse.ticket.token
    
    # return here & tell the user to call the endpoint to send the code to libreview
    
    


    return {"data": creds}
    
# ENDPOINT to submit the confirmation code & get the bearerToken 
    # send that code to the api
    # async with httpx.AsyncClient() as client:
    #     callback_url = "https://api-eu.libreview.io/auth/continue/2fa/result"
    #     resultCodeResponse = await client.post(callback_url)
    #     # this generates a NEW bearerToken as well
    #     bearerToken = resultCodeResponse.authTicket.token
    #     userId = resultCodeResponse.data.user.id
    
    # with this response, you should properly be able to get the user data
    
