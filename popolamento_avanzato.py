'''
Intestazione
'''

'''
import mysql.connector
from datetime import date, timedelta
import pandas as pd # Se non lo hai, installalo con pip install pandas

def populate_advanced_dims():
    try:
        db = mysql.connector.connect(
            host="localhost", user="root", password="easy22", database="CineData"
        )
        cursor = db.cursor()
        print("Connessione OK. Generazione Dim_Calendar...")

        # 1. Generazione Tabella Calendario (3 anni di dati)
        start_date = date(2023, 1, 1)
        end_date = date(2025, 12, 31)
        current = start_date
        
        calendar_data = []
        while current <= end_date:
            calendar_data.append((
                current,
                current.year,
                current.month,
                current.strftime('%B'), # Nome mese in inglese
                current.day,
                current.strftime('%A'), # Nome giorno
                1 if current.weekday() >= 5 else 0, # Passa 1 se è weekend
                (current.month - 1) // 3 + 1 # Calcolo Trimestre
            ))
            current += timedelta(days=1)
        
        # Uso IGNORE per evitare errori se la rilanci
        query_cal = "INSERT IGNORE INTO Dim_Calendar VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(query_cal, calendar_data)
        db.commit()
        print(f"Calendario popolato: {len(calendar_data)} giorni inseriti.")

        # 2. Generazione Recensioni (Mocking Feedback)
        print("Generazione Recensioni utenti...")
        # Recuperiamo utenti e film esistenti
        cursor.execute("SELECT user_id FROM Users")
        users = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT movie_id FROM Movies")
        movies = [r[0] for r in cursor.fetchall()]

        import random
        from faker import Faker
        fake = Faker()

        reviews_data = []
        # Creiamo circa 1000 recensioni casuali
        for _ in range(1000):
            u_id = random.choice(users)
            m_id = random.choice(movies)
            reviews_data.append((
                u_id,
                m_id,
                random.randint(1, 5), # Voto da 1 a 5
                fake.sentence(nb_words=12), # Commento finto
                fake.date_between(start_date='-1y', end_date='today')
            ))

        query_rev = "INSERT INTO Reviews (user_id, movie_id, rating, comment, review_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(query_rev, reviews_data)
        db.commit()
        print("Recensioni inserite con successo!")

    except mysql.connector.Error as err:
        print(f"Errore: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    populate_advanced_dims()
'''

import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def populate_advanced_data():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="easy22", 
            database="CineData"
        )
        cursor = db.cursor()
        print("Connessione stabilita. Inizio procedure avanzate...")

        # --- 1. GENERAZIONE DIM_CALENDAR (Il cuore del Data Warehouse) ---
        # Creiamo la tabella se non esiste direttamente da qui per sicurezza
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Dim_Calendar (
                date_key DATE PRIMARY KEY,
                year INT,
                month INT,
                month_name VARCHAR(20),
                quarter INT,
                day_of_week VARCHAR(20),
                is_weekend TINYINT(1)
            )
        """)
        
        print("Popolamento Dim_Calendar (3 anni)...")
        start_date = datetime(2023, 1, 1)
        calendar_data = []
        for i in range(1095): # 3 anni
            curr_date = start_date + timedelta(days=i)
            calendar_data.append((
                curr_date.date(),
                curr_date.year,
                curr_date.month,
                curr_date.strftime('%B'),
                (curr_date.month - 1) // 3 + 1,
                curr_date.strftime('%A'),
                1 if curr_date.weekday() >= 5 else 0
            ))
        
        # Usiamo IGNORE per non avere errori se riesegui il codice
        cursor.executemany("INSERT IGNORE INTO Dim_Calendar VALUES (%s, %s, %s, %s, %s, %s, %s)", calendar_data)
        db.commit()

        # --- 2. GENERAZIONE RECENSIONI (Per Analisi Qualitativa) ---
        cursor.execute("CREATE TABLE IF NOT EXISTS User_Reviews ("
                       "review_id INT AUTO_INCREMENT PRIMARY KEY,"
                       "user_id INT,"
                       "movie_id INT,"
                       "rating INT,"
                       "comment TEXT,"
                       "review_date DATE,"
                       "FOREIGN KEY (user_id) REFERENCES Users(user_id),"
                       "FOREIGN KEY (movie_id) REFERENCES Movies(movie_id))")
        
        print("Generazione Recensioni utenti (Bulk mode)...")
        cursor.execute("SELECT user_id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT movie_id FROM Movies")
        movie_ids = [row[0] for row in cursor.fetchall()]

        reviews_data = []
        # Generiamo circa 2000 recensioni casuali
        for _ in range(2000):
            uid = random.choice(user_ids)
            mid = random.choice(movie_ids)
            rating = random.randint(1, 10)
            # Commenti realistici basati sul voto
            if rating > 8:
                comment = random.choice(["Masterpiece!", "Amazing visuals", "Must watch", "Incredible director"])
            elif rating < 4:
                comment = random.choice(["Boring", "Disappointing", "Too long", "Not my type"])
            else:
                comment = random.choice(["Good movie", "Entertaining", "Solid acting", "Average"])
                
            reviews_data.append((uid, mid, rating, comment, fake.date_between(start_date='-1y', end_date='today')))

        cursor.executemany("INSERT INTO User_Reviews (user_id, movie_id, rating, comment, review_date) VALUES (%s, %s, %s, %s, %s)", reviews_data)
        db.commit()

        print(f"SUCCESS! Inserite {len(calendar_data)} date e {len(reviews_data)} recensioni in pochi secondi.")

    except mysql.connector.Error as err:
        print(f"Errore: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    populate_advanced_data()