from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import key


app = FastAPI()

@app.get("/")
def getAllData():
    return Sheets.get_all_records()

@app.get("/users/{userName}")
def findName(userName: str):
    cell = Sheets.find(userName)
    if not cell:
        raise HTTPException(status_code=404, detail="User not found")
    return Sheets.row_values(cell.row)


class Info(BaseModel):
    id: int
    data: list


@app.post("/addNewUser")
def getInformation(info: Info):
    Sheets.append_row(info.data)
    return {"status": "SUCCESS", "data": info}


@app.put("/users/{name}/{account}")
def update_account(name: str, account: str):
    cell = Sheets.find(name)
    if not cell:
        raise HTTPException(status_code=404, detail="User not found")
    r = cell.row
    Sheets.update(f"B{r}", account)   # 更改sheet中B4儲存格的值(假設找到account位於row4)
    return {"msg": Sheets.row_values(r)}


import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
Json = "calendar.json"
Url = ["https://spreadsheets.google.com/feeds"]
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)
Sheet = GoogleSheets.open_by_key(key.google_sheet_key)
Sheets = Sheet.sheet1

# # pandas
# import pandas as pd
# dataframe = pd.DataFrame(Sheets.get_all_records())
# print(dataframe)