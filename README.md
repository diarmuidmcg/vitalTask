# vitalTask

fastAPI codebase for the tryVital.io Task

to run:

- install all packages
  - if theres a `pip3 install` like `npm i` then run that, otherwise
    `pip3 install typing fastapi pydantic httpx bs4 json re datetime time sqlmodel`

Breakdown of solution:

- Pass the `email` & `password` BODY parameters into the POST /signin endpoint
  -> this calls the LibreView /login endpoint
  -> it then calls the LibreView /sendCode endpoint to generate a 2fa code
  -> this will return a bearerToken & will send an email with the 2fa code
- Then pass the `accessCode` & `bearerToken` BODY parameters into the POST /enter-code endpoint
  -> this calls the LibreView /result endpoint to verify the account
  -> it then calls the LibreView /dashboard endpoint to get the patientIds
  -> then it calls my query_libre() function
- the query_libre() function fetches the data & stores it in a sqlite database
  -> this calls the LibreView /reports endpoint to get a new access token & url
  -> call this next url, this then gets ANOTHER url to call
  -> this url retreives al the reports based on the data you queryed for. it rerturns another link to call
  -> this url retreives the data in HTML format. I parsed the data into js & then JSON
  -> once in JSON, i iterate through the Days[n]Glucose data & add each timestamp, value, & patientId to a GlucoseDataPoint model & store it the SQLite database
- Once each patient's data has been stored, the /glucose endpoint can be called
- the /glucose endpoint takes in a start_date & end_date as QUERY parameters & returns the data

Corners I cut:

- I would like to have an optional parameter PatientId on the /glucose endpoint so that you can query depending on the patient
- I would have better endpoint responses that contain data & proper response codes
- The project would be multiple folders & would be separated by function. I'm a big fan of Nest.js & opinionated structures so my ideal structure would look something like
  main.py
  auth
  main.py
  controller.py
  helperfunctions.py
  data-generation
  main.py
  controller.py
  helperfunctions.py
  However, I'm not entirely sure if separating routes from code is a common thing with FastAPI
- Storing database in just a db file (& not using a .env file to store its name)

What I learned throughout this challenge

- Python (I've never used it)
  - Syntax
  - fastAPI
  - pydantic
  - httpx
- Using a model to create a database table (I always just have an entity file for a backend)
- Parsing HTML response into JSON & then eventually Python (basically webscraping)
- Reverse engineering ANYTHING

I list all that not because I want you to take it easy on me. I don't.
I just want to demonstrate that I'm a fast learner!
