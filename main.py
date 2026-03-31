from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import random
import math
import uvicorn
from pathlib import Path
import sqlite3
from datetime import datetime


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/images", StaticFiles(directory=BASE_DIR / "images"), name="images")

# Data storage
countries = {
    "Albania": {"rating": 1500, "games": 0, "photo": "images/albania.jpg", "name": "Alis Kallaci"},
    "Armenia": {"rating": 1500, "games": 0, "photo": "images/armenia.jpg", "name": "Simon Hovhannisyan"},
    "Austria": {"rating": 1500, "games": 0, "photo": "images/austria.jpg", "name": "Benjamin Gedeon"},
    "Czechia": {"rating": 1500, "games": 0, "photo": "images/czechia.jpg", "name": "Daniel Zizka"},
    "Denmark": {"rating": 1500, "games": 0, "photo": "images/denmark.jpg", "name": "Søren Torpegaard Lund"},
    "Finland": {"rating": 1500, "games": 0, "photo": "images/finland.jpg", "name": "Pete Eemeli Parkkonen"},
    "Greece": {"rating": 1500, "games": 0, "photo": "images/greece.jpg", "name": "Akylas"},
    "Israel": {"rating": 1500, "games": 0, "photo": "images/israel.jpg", "name": "Noam Bettan"},
    "Italy": {"rating": 1500, "games": 0, "photo": "images/italy.jpg", "name": "Salvatore Michael Sorrentino"},
    "Lithuania": {"rating": 1500, "games": 0, "photo": "images/lithuania.jpg", "name": "Tomas Alenčikas"},
    "Malta": {"rating": 1500, "games": 0, "photo": "images/malta.jpg", "name": "Aidan Cassar"},
    "Moldova": {"rating": 1500, "games": 0, "photo": "images/moldova.jpg", "name": "Vlad Sabajuc"},
    "Norway": {"rating": 1500, "games": 0, "photo": "images/norway.jpg", "name": "Jonas Lovv Hellesøy"},
    "Serbia": {"rating": 1500, "games": 0, "photo": "images/serbia.jpg", "name": "Luka Aranđelović"},
    "United Kingdom": {"rating": 1500, "games": 0, "photo": "images/uk.jpg", "name": "Sam Bartle"}
}


# load data from database
def load_data():
    conn = sqlite3.connect("eurovision.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, rating, games, photo, artist FROM countries")
    rows = cursor.fetchall()
    for row in rows:
        countries[row[0]] = {
            "rating": row[1],
            "games": row[2],
            "photo": row[3],
            "name": row[4]
        }
    conn.close()
    return countries

countries = load_data()


current_pair = None

class VoteRequest(BaseModel):
    winner: int

def calculate_elo(winner_rating, loser_rating, k=32):
    expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
    new_winner = winner_rating + k * (1 - expected_winner)
    new_loser = loser_rating + k * (0 - (1 - expected_winner))
    return round(new_winner), round(new_loser)

def get_new_pair():
    country_list = list(countries.keys())
    return random.sample(country_list, 2)

@app.get("/api/comparison")
def get_comparison():
    global current_pair
    if not current_pair:
        current_pair = get_new_pair()
    
    return {
        "country1": {"name": current_pair[0], "rating": countries[current_pair[0]]["rating"], "photo": countries[current_pair[0]]["photo"], "artist_name": countries[current_pair[0]]["name"]},
        "country2": {"name": current_pair[1], "rating": countries[current_pair[1]]["rating"], "photo": countries[current_pair[1]]["photo"], "artist_name": countries[current_pair[1]]["name"]}
    }

@app.post("/api/vote")
def vote(vote_request: VoteRequest):
    global current_pair
    if not current_pair:
        return {"error": "No comparison available"}
    
    winner = current_pair[vote_request.winner - 1]
    loser = current_pair[2 - vote_request.winner]
    
    winner_elo, loser_elo = calculate_elo(
        countries[winner]["rating"],
        countries[loser]["rating"]
    )
    
    countries[winner]["rating"] = winner_elo
    countries[winner]["games"] += 1
    countries[loser]["rating"] = loser_elo
    countries[loser]["games"] += 1
    
    current_pair = get_new_pair()

    # update database
    conn = sqlite3.connect("eurovision.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE countries SET rating = ?, games = ? WHERE name = ?", (countries[winner]["rating"], countries[winner]["games"], winner))
    cursor.execute("UPDATE countries SET rating = ?, games = ? WHERE name = ?", (countries[loser]["rating"], countries[loser]["games"], loser))
    conn.commit()
    conn.close()

    
    return {"success": True}

@app.api_route("/api/data", methods=["GET", "POST"])
async def data():
    return {"ok": True}

@app.get("/api/top")
def get_top():
    sorted_countries = sorted(
        countries.items(),
        key=lambda x: x[1]["rating"],
        reverse=True
    )
    return sorted_countries
'''[
        {"name": name, "rating": data["rating"]}
        for name, data in sorted_countries
        
    ]'''

@app.get("/")
def read_root():
    return FileResponse("index.html")
