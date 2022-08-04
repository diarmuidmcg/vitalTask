from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import httpx


# async await for api reqs
client = httpx.AsyncClient(verify=False)

class SignInObject(BaseModel):
    email: str
    password: str
    
class EnterCodeObject(BaseModel):
    accessCode: int
    bearerToken: str

# sign in function that will pass take a username & password & send it to 
# LibreView
@app.post("/signin")
async def sign_in_user(creds: SignInObject):
    
    # may need to call this func to set to gb
    # callback_url = "https://api-eu.libreview.io/config"
        
    # create body object
    signInBody={
        "Country":"GB",
        "email": creds.email,
        "password": creds.password
        }
    # convert to json
    jsonData = json.dumps(signInBody)

    try:
        headers = {"Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
        callback_url = "https://api-eu.libreview.io/auth/login"
        initialSignIn = await client.post(callback_url, data=jsonData, headers=headers)
        loginResponse = initialSignIn.json()
        bearerToken = loginResponse["data"]["authTicket"]["token"]
        verify = loginResponse["data"]["step"]
        print(loginResponse)
    except httpx.RequestError as exc:
        return { "error": f"An error occurred while requesting {exc.request.url!r}." }
    except httpx.HTTPStatusError as exc:
        return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
    except:
        return {"error": f"Error response {initialSignIn.content} while requesting {callback_url}." }

    # IF the user is not remembered (needs confirmation token)
    
    if verify["type"] == "2faVerify":
        # create body object
        verifyObject={
            "isPrimaryMethod":False
            }
        # convert to json
        jsonData = json.dumps(verifyObject)
        try:
            # generate the access token to be sent to the email
            headers = {'Authorization': 'Bearer ' + bearerToken, "Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
            callback_url = "https://api-eu.libreview.io/auth/continue/2fa/sendcode"
            generateCode = await client.post(callback_url, data=jsonData, headers=headers)
            sendCodeResponse = generateCode.json()
            # this generates a NEW bearerToken as well
            bearerToken = sendCodeResponse["ticket"]["token"]
            # print(sendCodeResponse)
        except httpx.RequestError as exc:
            return { "error": f"An error occurred while requesting {exc.request.url!r}." }
        except httpx.HTTPStatusError as exc:
            return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
        except:
            return {"error": f"Error response {generateCode.content} while requesting {callback_url}." }
        
    # return here & tell the user to call the endpoint to send the code to libreview

    return {"data": f"call the /enter-code endpoint & in the body pass the code & bearerToken {bearerToken}"}
    
# sign in function that will pass take a username & password & send it to 
# LibreView
@app.post("/enter-code")
async def enter_code(token: EnterCodeObject):
    
    # create body object
    verifyObject={
        "code": str(token.accessCode),
        "isPrimaryMethod": False,
        }
    # convert to json
    jsonData = json.dumps(verifyObject)
    print(token.bearerToken)
    print(jsonData)
    try:
        headers = {'Authorization': 'Bearer ' + token.bearerToken, "Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
        callback_url = "https://api-eu.libreview.io/auth/continue/2fa/result"
        finalSignIn = await client.post(callback_url, data=jsonData, headers=headers)
        loginResponse = finalSignIn.json()
        bearerToken = loginResponse["data"]["authTicket"]["token"]
        professionalId = loginResponse["data"]["user"]["id"]
        print(loginResponse)
    except httpx.RequestError as exc:
        return { "error": f"An error occurred while requesting {exc.request.url!r}." }
    except httpx.HTTPStatusError as exc:
        return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
    except:
        return {"error": f"Error response {finalSignIn.content} while requesting {callback_url}." }
    


    dashboardObject={
        "filters":[],
        "columns":[
            "lastAvailableData",
            "avgGlucose",
            "sensorDailyScans",
            "percentGlucoseInTarget",
            "libreViewStatus"
            ],
        "interval":"14",
        "view":"Dashboard.allPatients",
        "count":50,
        "page":1,
        "searching":{},
        "sort":{
            "desc":False,"key":"firstName"
        }
    }
    # convert to json
    jsonData = json.dumps(dashboardObject)

    # call /dashboard to get the patientIds & information 
    try:
        headers = {'Authorization': 'Bearer ' + bearerToken, "Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
        callback_url = "https://api-eu.libreview.io/dashboard"
        dashboardData = await client.post(callback_url, data=jsonData, headers=headers)
        dashboardResponse = dashboardData.json()
        # get patient info
        patients = dashboardResponse["data"]["results"]
        patientIds = []
        # iterate thru & collect all patient ids
        for patient in patients:
            patientIds.append(patient["id"])
        print(dashboardResponse)
    except httpx.RequestError as exc:
        return { "error": f"An error occurred while requesting {exc.request.url!r}." }
    except httpx.HTTPStatusError as exc:
        return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
    except:
        return {"error": f"Error response {dashboardData.content} while requesting {callback_url}." }


    # for each patient, add their information to the db
    
    # get last 6 months of data
    # calc the date today in epoch
    todayDate = int(time.time())
    # 1 month = 2629743
    # 1 month x 6
    differenceInMonths = int(2629743 * 6)
    startDate = todayDate - differenceInMonths
    
    for patient in patientIds:
        await query_libre(startDate,todayDate,bearerToken,patient,professionalId)
        print("got data for patient " + patient)

    return {"data": "finished"}


