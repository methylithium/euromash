import sqlite3

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
conn = sqlite3.connect('eurovision.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        rating INTEGER,
        games INTEGER,
        photo TEXT,
        artist TEXT
    )
''')

for country, data in countries.items():
    cursor.execute('''
        INSERT INTO countries (name, rating, games, photo, artist)
        VALUES (?, ?, ?, ?, ?)
    ''', (country, data['rating'], data['games'], data['photo'], data['name']))

conn.commit()
conn.close()