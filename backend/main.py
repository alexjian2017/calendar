import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from fastapi import FastAPI, HTTPException
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


@app.post("/addNewEvent")
def getInformation(info: Info):
    Sheets.append_row(info.data)
    return {"status": "SUCCESS", "data": info}
