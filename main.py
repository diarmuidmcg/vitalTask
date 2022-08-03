from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import httpx


app = FastAPI()

bearerToken = ""

# GLOBAL VARS
patientId = "3f5e19e1-d667-11ea-a179-0242ac110007"
professionalId = "43dd94c6-fc1e-11eb-ba23-0242ac110004"

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
    
async def query_libre(start_date: int, end_date: int):
    
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
        "PrintReportsWithPatientInformation":false,
        "ReportIds":[540066],
        "SecondaryDeviceIds":["0bebe0fc-2b58-11ec-895a-0242ac110005","63055cd4-f7b2-11eb-951b-0242ac110002","67ccf8be-e63a-11eb-a26e-0242ac110002","3c41cd72-e633-11eb-a26e-0242ac110002","93b9f4f0-e5c2-11eb-951b-0242ac110002","baa36267-d66f-11ea-8740-0242ac110003"],
        "TertiaryDeviceIds":[],
        "ConnectedInsulinDeviceIds":[],
        "StartDates":[start_date],
        "TargetRangeHigh":10,
        "TargetRangeLow":3.8,
        "TimeFormat":2,
        "TodayDate":todayDate,
        "PatientDateOfBirth":745632000,
        "PatientId":patientId,
        "ProfessionalId":professionalId,
        "ClientReportIDs":[5]
        }
    # POST 
    # This generates the overall report
    async with httpx.AsyncClient() as client:
        callback_url = "https://api-eu.libreview.io/reports"
        postReport = await client.post(callback_url, data=postReportData)
        bearerToken = postReport.ticket.token
        # this url is the next endpoint to call
        channelUrl = postReport.data.url
        # print(postReport.json())
        
    # GET 
    # This generates the link to retreive the data from numerous reports
    async with httpx.AsyncClient() as client:
        getChannel = await client.get(channelUrl)
        # this url is the next endpoint to call
        dataIpUrl = getChannel.data.lp
        # print(getChannel.json())
        
    # GET 
    # This generates the links to those reports
    async with httpx.AsyncClient() as client:
        getReports = await client.get(dataIpUrl)
        # this url is the next endpoint to call
        properReportUrl = getReports.url["5"]
        # print(getChannel.json())
        
    # GET 
    # This generates the final report as a file that contains the data
    async with httpx.AsyncClient() as client:
        # the endpoint takes a query parameter as the bearerToken
        dataInJavascriptFile = await client.get(properReportUrl+"?session="+bearerToken)
        # the data is in this return data, must parse
        properReportUrl = dataInJavascriptFile
        # print(getChannel.json())
