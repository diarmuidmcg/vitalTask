from typing import Union, Optional
from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings
# for async await http resquests
import httpx

# for converting html response to actual variable values
from bs4 import BeautifulSoup
import json
import re

# used for validating current date & converting dates to epoch time
import datetime
import time
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


from sqlmodel import Field, Session, SQLModel, create_engine, select

# model for glucose data points
class GlucoseDataPoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: int
    value: float
    patientId: str

app = FastAPI()

# async await for api reqs
client = httpx.AsyncClient(verify=False)

# main function that'll return all the data requested from the data pool
@app.get("/glucose")
async def get_glucose(start_date: str, end_date: str):
    
    # validate that the start date & end date are the proper YYYY-MM-DD format
    # and that they are all valid numbers / years
    try:
        validate(start_date)
    except:
        return {"error": "state date should be YYYY-MM-DD & a query parameter"}
    try:
        validate(end_date)
    except:
        return {"error": "end date should be YYYY-MM-DD & a query parameter"}
    
    # convert YYYY-MM-DD to epoch timestamp
    # convert it to int to remove trailing 0 & decimal
    epochStart = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    epochEnd = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    
    engine = create_engine("sqlite:///GlucoseData.db")
    # get datapoints within bounds
    with Session(engine) as session:
        statement = select(GlucoseDataPoint).where(GlucoseDataPoint.timestamp > epochStart).where(GlucoseDataPoint.timestamp < epochEnd)
        glucose = session.exec(statement).all()
        
    # if no data is returned, prompt the user to change the parameters
    if len(glucose) == 0:
        return {"data": "No data was returned, try changing your parameters"}
    # return those datapoints
    return {"data": glucose}
    


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

    return {"data": "call the /enter-code endpoint & in the BODY pass the code & bearerToken","bearerToken":bearerToken}
    
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
    try:
        headers = {'Authorization': 'Bearer ' + token.bearerToken, "Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
        callback_url = "https://api-eu.libreview.io/auth/continue/2fa/result"
        finalSignIn = await client.post(callback_url, data=jsonData, headers=headers)
        loginResponse = finalSignIn.json()
        bearerToken = loginResponse["data"]["authTicket"]["token"]
        professionalId = loginResponse["data"]["user"]["id"]
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

    return {"data": "You can now query the /glucose endpoint to get the data you need"}

# this function querys LibreView to access the data for each patient
async def query_libre(start_date: int, end_date: int, bearerToken: str, patientId: str, professionalId: str):
    
    # calc the date today in epoch
    todayDate = int(time.time())
    
    # create body object
    postReportData={
        "Country":"GB",
        "CultureCode":"en-GB",
        "CultureCodeCommunication":"en-GB",
        "DateFormat":2,
        "EndDate":end_date,
        "GlucoseUnits":0,
        "HighGlucoseThreshold":13.9,
        "LowGlucoseThreshold":2.8,
        "PrimaryDeviceId":"9ce4ef20-b9c1-11ec-b614-0242ac11000b",
        "PrimaryDeviceTypeId":40066,
        "PrintReportsWithPatientInformation":False,
        "ReportIds":[540066],
        "SecondaryDeviceIds":["0bebe0fc-2b58-11ec-895a-0242ac110005","63055cd4-f7b2-11eb-951b-0242ac110002","67ccf8be-e63a-11eb-a26e-0242ac110002","3c41cd72-e633-11eb-a26e-0242ac110002","93b9f4f0-e5c2-11eb-951b-0242ac110002","baa36267-d66f-11ea-8740-0242ac110003"],
        "StartDates":[start_date],
        "TargetRangeHigh":10,
        "TargetRangeLow":3.8,
        "TimeFormat":2,
        "TodayDate":todayDate,
        "PatientId":patientId,
        "ProfessionalId":professionalId,
        "ClientReportIDs":[5]
        }
    # convert to json
    jsonData = json.dumps(postReportData)
    
    # POST 
    # This generates the overall report
    headers = {'Authorization': 'Bearer ' + bearerToken, "Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    # headers = {'Authorization': bearerToken}
    callback_url = "https://api-eu.libreview.io/reports"
    try:
        postReport = await client.post(callback_url, data=jsonData, headers=headers)
        postReportJson = postReport.json()
        # the token thats returned must be used as the session value for the last call
        bearerToken = postReportJson["ticket"]["token"]
        # this url is the next endpoint to call
        channelUrl = postReportJson["data"]["url"]
    except httpx.RequestError as exc:
        return { "error": f"An error occurred while requesting {exc.request.url!r}." }
    except httpx.HTTPStatusError as exc:
        return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
    except:
        return {"error": f"Error response {postReport.content} while requesting {callback_url}." }
    

    # GET 
    # This generates the link to retreive the data from numerous reports
    try:
        getChannel = await client.get(channelUrl, headers=headers)
        getChannelJson = getChannel.json()
        # this url is the next endpoint to call
        dataIpUrl = getChannelJson["data"]["lp"]
    except httpx.RequestError as exc:
        return { "error": f"An error occurred while requesting {exc.request.url!r}." }
    except httpx.HTTPStatusError as exc:
        return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
    except:
        return {"error": f"Error response {getChannel.content} while requesting {channelUrl}." }


    # GET 
    # This generates the links to those reports
    try:
        getReports = await client.get(dataIpUrl, headers=headers)
        getReportsJson = getReports.json()
        # this url is the next endpoint to call
        properReportUrl = getReportsJson["args"]["urls"]["5"]
    except httpx.RequestError as exc:
        return { "error": f"An error occurred while requesting {exc.request.url!r}." }
    except httpx.HTTPStatusError as exc:
        return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
    except:
        return {"error": f"Error response {getReports.content} while requesting {dataIpUrl}." }
        
    # GET 
    # This generates the final report as a file that contains the data
    # the endpoint takes a query parameter as the bearerToken
    try:
        dataInJavascriptFile = await client.get(properReportUrl+"?session="+bearerToken, headers=headers)
    except httpx.RequestError as exc:
        return { "error": f"An error occurred while requesting {exc.request.url!r}." }
    except httpx.HTTPStatusError as exc:
        return { "error": f"Error response {exc.response.status_code} while requesting {exc.request.url!r}." }
    except:
        return {"error": f"Error response {dataInJavascriptFile.content} while requesting {properReportUrl}." }
    
    try:
        # parse html response 
        soup = BeautifulSoup(dataInJavascriptFile.text, 'lxml')
        # get correct script tag
        rows = soup.head.findAll('script')[4::5]
        scriptTag = str(rows[1])
        # search the script tag for the variable 'window.Report'
        search = re.search(r'window.Report = ([\s\S]+)?',scriptTag).group(1)
        # must remove the closing script tag
        completeObject = search.replace("</script>","").replace(";","")
        # convert the string into json
        object = json.loads(completeObject)
        
        # create the database
        engine = create_engine("sqlite:///GlucoseData.db")
        SQLModel.metadata.create_all(engine)
        
        # now iterate through Data.Days & get all the glucose data
        # glucoseData = []
        days = object["Data"]["Days"]
        # get each individial day
        for day in days:
            # theres a second bracket before the glucose data
            for dataGroup in day["Glucose"]:
                # this is each individial piece of data
                for dataPoint in dataGroup:
                    # create a model instance 
                    glucose = GlucoseDataPoint(timestamp=dataPoint["Timestamp"],value=dataPoint["Value"],patientId=patientId)
                    # save it 
                    with Session(engine) as session:
                        session.add(glucose)
                        session.commit()
    except:
        return {"error": "there was an issue parsing the data returned from the api"}

    return {"data":"the data was successfully stored"}

