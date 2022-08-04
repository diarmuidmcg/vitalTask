from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings

# for async await http resquests
import httpx

# for converting html response to actual variable values
from bs4 import BeautifulSoup
import json
import re

class Token(BaseSettings):
    bearerToken: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQzZGQ5NGM2LWZjMWUtMTFlYi1iYTIzLTAyNDJhYzExMDAwNCIsImZpcnN0TmFtZSI6InRhc2siLCJsYXN0TmFtZSI6InRyeXZ0YWlsIiwiY291bnRyeSI6IkdCIiwicmVnaW9uIjoiZXUiLCJyb2xlIjoiaGNwIiwidW5pdHMiOjAsInByYWN0aWNlcyI6W10sImMiOjEsInMiOiJsdiIsImV4cCI6MTY1OTU3ODQxM30.FCy_wkjIUjpj6gC10UxQvxPXM8YNmAG2knC6T4EyORE"


app = FastAPI()

client = httpx.AsyncClient(verify=False)

# bearerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQzZGQ5NGM2LWZjMWUtMTFlYi1iYTIzLTAyNDJhYzExMDAwNCIsImZpcnN0TmFtZSI6InRhc2siLCJsYXN0TmFtZSI6InRyeXZ0YWlsIiwiY291bnRyeSI6IkdCIiwicmVnaW9uIjoiZXUiLCJyb2xlIjoiaGNwIiwidW5pdHMiOjAsInByYWN0aWNlcyI6W10sImMiOjEsInMiOiJsdiIsImV4cCI6MTY1OTU3ODQxM30.FCy_wkjIUjpj6gC10UxQvxPXM8YNmAG2knC6T4EyORE"

# GLOBAL VARS
patientId = "3f5e19e1-d667-11ea-a179-0242ac110007"
professionalId = "43dd94c6-fc1e-11eb-ba23-0242ac110004"

# main function that'll return all the data requested from the data pool
@app.get("/glucose")
async def get_glucose(start_date: str = "", end_date: str = ""):
    
    # ensure signed in 
        # if not, prompt user to call /signin endpoint
    
    # ensure params includes
    # if not start_date or not end_date:
    #     return {"error": "You did not pass in the correct parameters"}
    # validate that the start date & end date are the proper YYYY-MM-DD format
    # and that they are all valid numbers / years
    
    
    # ensure the data has been loaded
        # if not, prompt user to call the /generate-data endpoint 
    
    
    # search data pool based on parameters passed in
    await query_libre(1650052354, 1650326400)

    
    data = start_date + end_date
    return {"data": data}
    
async def query_libre(start_date: int, end_date: int):
    bearerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQzZGQ5NGM2LWZjMWUtMTFlYi1iYTIzLTAyNDJhYzExMDAwNCIsImZpcnN0TmFtZSI6InRhc2siLCJsYXN0TmFtZSI6InRyeXZ0YWlsIiwiY291bnRyeSI6IkdCIiwicmVnaW9uIjoiZXUiLCJyb2xlIjoiaGNwIiwidW5pdHMiOjAsInByYWN0aWNlcyI6W10sImMiOjEsInMiOiJsdiIsImV4cCI6MTY1OTU3ODQxM30.FCy_wkjIUjpj6gC10UxQvxPXM8YNmAG2knC6T4EyORE"

    print("i got here")
    # calc the date today in epoch
    todayDate = 1659484800
    
    # first thing first is 
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
    jsonData = json.dumps(postReportData)
    print("i even got here")
    # POST 
    # This generates the overall report
    
    print("into async client")
    headers = {'Authorization': 'Bearer ' + bearerToken, "Content-Type":"application/json", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    # headers = {'Authorization': bearerToken}
    callback_url = "https://api-eu.libreview.io/reports"
    postReport = await client.post(callback_url, data=jsonData, headers=headers)
    postReportJson = postReport.json()
    print(postReportJson)
    bearerToken = postReportJson["ticket"]["token"]
    # this url is the next endpoint to call
    channelUrl = postReportJson["data"]["url"]

        
    # GET 
    # This generates the link to retreive the data from numerous reports
    
    getChannel = await client.get(channelUrl, headers=headers)
    getChannelJson = getChannel.json()
    print(getChannelJson)
    # this url is the next endpoint to call
    dataIpUrl = getChannelJson["data"]["lp"]

        
    # GET 
    # This generates the links to those reports
    
    getReports = await client.get(dataIpUrl, headers=headers)
    getReportsJson = getReports.json()
    print(getReportsJson)
    print("got to args url")
    # this url is the next endpoint to call
    properReportUrl = getReportsJson["args"]["urls"]["5"]
    print("made it json")
        
    # GET 
    # This generates the final report as a file that contains the data
    
    # the endpoint takes a query parameter as the bearerToken
    dataInJavascriptFile = await client.get(properReportUrl+"?session="+bearerToken, headers=headers)
    print("made it to js file")

    
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
    
    # now iterate through Data.Days & get all the glucose data
    print(object["Data"]["Days"])
