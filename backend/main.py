import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import key


Json = "calendar.json"
Url = ["https://spreadsheets.google.com/feeds"]
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
Sheet = GoogleSheets.open_by_key(key.google_sheet_key)
Sheets = Sheet.sheet1

app = FastAPI()

@app.get("/")
def getAllData():
    return Sheets.get_all_records()

class Info(BaseModel):
    id: int
    data: list

@app.post("/addNewEvents")
def getInformation(info: Info):
    if info.data[1] and info.data[2]:
        Sheets.append_row(info.data)
        return {"status": "SUCCESS", "data": info}
    return {"status": "ERROR", "data": info}

# accept the frontend request
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
