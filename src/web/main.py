import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
templates = Jinja2Templates(directory="src/web/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    conn = sqlite3.connect('src/database/signals.db')
    c = conn.cursor()
    c.execute("SELECT * FROM signals ORDER BY timestamp DESC LIMIT 50")
    signals = [{"pair": r[0], "type": r[1], "entry": r[2], "tps": json.loads(r[3]), 
                "sl": r[4], "leverage": r[5], "timeframe": r[6], "timestamp": r[7]} for r in c.fetchall()]
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "signals": signals})
