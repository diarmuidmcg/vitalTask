from typing import Union
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


class GlucoseDataPoint:
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value


app = FastAPI()
# async await for api reqs
client = httpx.AsyncClient(verify=False)

# body object for glucose api call
class GlucoseBody(BaseModel):
    bearerToken: str
    patientId: str
    professionalId: str

# main function that'll return all the data requested from the data pool
@app.get("/glucose")
async def get_glucose(start_date: str, end_date: str, glucoseBody: GlucoseBody):
    
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
    
    # validate the bearerToken isnt expired
    
    # ensure the data has been loaded
        # if not, prompt user to call the /generate-data endpoint 
    
    
    # search data pool based on parameters passed in
    data = await query_libre(epochStart, epochEnd, glucoseBody.bearerToken, glucoseBody.patientId, glucoseBody.professionalId)

    # data = "testing"
    return {"data": data}
    
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
        
        # now iterate through Data.Days & get all the glucose data
        glucoseData = []
        days = object["Data"]["Days"]
        # get each individial day
        for day in days:
            # theres a second bracket before the glucose data
            for dataGroup in day["Glucose"]:
                # this is each individial piece of data
                for dataPoint in dataGroup:
                    glucose = GlucoseDataPoint(dataPoint["Timestamp"],dataPoint["Value"])
                    glucoseData.append(glucose)
    except:
        return {"error": "there was an issue parsing the data returned from the api"}
        
    # allGlucose = db.GqlQuery("SELECT *", 100)

    return glucoseData


