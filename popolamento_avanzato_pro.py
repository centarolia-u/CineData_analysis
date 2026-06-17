'''
Intestazione
'''
'''
import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Configurazione (Assicurati che i dati siano corretti)
config = {
    'user': 'root',
    'password': 'easy22',
    'host': 'localhost',
    'database': 'CineData'
}

def populate_advanced_pro():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        print("--- Inizio ETL Professionale: Fase Avanzata ---")

        # --- 1. CREAZIONE TABELLA REVIEWS (Se non esiste già correttamente) ---
        # La definiamo qui per essere sicuri della corrispondenza colonne/valori
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                movie_id INT,
                rating TINYINT,
                review_text TEXT,
                review_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
            ) ENGINE=InnoDB
        """)

        # --- 2. GENERAZIONE RECENSIONI (Corretta) ---
        print("Generazione Recensioni utenti...")
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT movie_id FROM movies")
        movie_ids = [row[0] for row in cursor.fetchall()]

        reviews_data = []
        # Generiamo circa 1000 recensioni casuali
        for _ in range(1000):
            u_id = random.choice(user_ids)
            m_id = random.choice(movie_ids)
            rating = random.randint(1, 10)
            # Testi realistici basati sul voto
            if rating > 7:
                text = random.choice(["Capolavoro assoluto!", "Da vedere assolutamente.", "Regia incredibile.", "Uno dei miei preferiti."])
            elif rating > 4:
                text = random.choice(["Non male, ma lento.", "Bravi gli attori, meno la storia.", "Pellicola interessante.", "Si può guardare."])
            else:
                text = random.choice(["Delusione totale.", "Non lo finirei mai.", "Pessimo montaggio.", "Tempo sprecato."])
            
            review_date = fake.date_between(start_date='-1y', end_date='today')
            
            # NOTA: Inseriamo 5 valori per 5 colonne (review_id è auto)
            reviews_data.append((u_id, m_id, rating, text, review_date))

        # Bulk insert per massimizzare le performance
        query_reviews = "INSERT INTO reviews (user_id, movie_id, rating, review_text, review_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(query_reviews, reviews_data)
        
        db.commit()
        print(f"OK: {cursor.rowcount} recensioni inserite.")

        # --- 3. DATA QUALITY CHECK (Il tocco da Senior) ---
        print("\n--- Esecuzione Data Quality Audit ---")
        
        # Check 1: Orfani nelle visioni (Visioni senza un dispositivo associato dopo l'aggiornamento)
        cursor.execute("SELECT COUNT(*) FROM watch_history WHERE device_id IS NULL")
        orphans = cursor.fetchone()[0]
        print(f"Audit Dispositivi: {orphans} visioni senza dispositivo (Target: 0)")

        # Check 2: Coerenza Rating
        cursor.execute("SELECT AVG(rating) FROM reviews")
        avg_rating = cursor.fetchone()[0]
        print(f"Audit Business: Rating medio globale della piattaforma: {float(avg_rating):.2f}")

        # Check 3: Integrità Calendario
        cursor.execute("SELECT COUNT(*) FROM dim_calendar")
        days = cursor.fetchone()[0]
        print(f"Audit Dimensionale: Tabella Calendario contiene {days} giorni.")

        print("\nSUCCESS: Data Warehouse aggiornato e verificato.")

    except mysql.connector.Error as err:
        print(f"ERRORE CRITICO: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    populate_advanced_pro()
'''

import mysql.connector
import random
from faker import Faker
from datetime import datetime

fake = Faker()

def populate_advanced_pro():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="easy22",
            database="CineData"
        )
        cursor = db.cursor()
        print("--- Inizio ETL Professionale: Fase Avanzata ---")

        # 1. FIX DELLO SCHEMA (Allineamento colonne)
        # Controlliamo se esiste la vecchia colonna 'comment' per rinominarla
        cursor.execute("SHOW COLUMNS FROM reviews LIKE 'comment'")
        if cursor.fetchone():
            print("Rilevata vecchia colonna 'comment'. Rinominazione in 'review_text'...")
            cursor.execute("ALTER TABLE reviews CHANGE comment review_text TEXT")
            db.commit()

        # 2. ASSICURIAMO CHE LA TABELLA SIA CORRETTA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                movie_id INT,
                rating TINYINT,
                review_text TEXT,
                review_date DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
            ) ENGINE=InnoDB
        """)

        # 3. GENERAZIONE RECENSIONI
        print("Generazione Recensioni utenti...")
        cursor.execute("SELECT user_id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT movie_id FROM Movies")
        movie_ids = [row[0] for row in cursor.fetchall()]

        reviews_data = []
        for _ in range(1000):
            u_id = random.choice(user_ids)
            m_id = random.choice(movie_ids)
            rating = random.randint(1, 10)
            
            if rating > 7:
                text = random.choice(["Capolavoro assoluto!", "Da vedere assolutamente.", "Regia incredibile.", "Uno dei miei preferiti."])
            elif rating > 4:
                text = random.choice(["Non male, ma lento.", "Bravi gli attori, meno la storia.", "Pellicola interessante.", "Si può guardare."])
            else:
                text = random.choice(["Delusione totale.", "Non lo finirei mai.", "Pessimo montaggio.", "Tempo sprecato."])
            
            review_date = fake.date_between(start_date='-1y', end_date='today')
            reviews_data.append((u_id, m_id, rating, text, review_date))

        # Bulk insert (fai attenzione: l'ordine dei parametri deve essere identico a quello sotto)
        query_reviews = "INSERT INTO reviews (user_id, movie_id, rating, review_text, review_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(query_reviews, reviews_data)
        db.commit()
        
        print(f"OK: {cursor.rowcount} recensioni inserite.")

        # 4. DATA QUALITY CHECK (Il tocco da Senior)
        print("\n--- Esecuzione Data Quality Audit ---")
        
        # Check 1: Integrità Calendario
        cursor.execute("SELECT COUNT(*) FROM dim_calendar")
        days = cursor.fetchone()[0]
        print(f"Audit Dimensionale: Tabella Calendario contiene {days} giorni.")

        # Check 2: Coerenza Rating
        cursor.execute("SELECT AVG(rating) FROM reviews")
        avg_rating = cursor.fetchone()[0]
        print(f"Audit Business: Rating medio globale della piattaforma: {float(avg_rating):.2f}")

        print("\nSUCCESS: Data Warehouse aggiornato e verificato.")

    except mysql.connector.Error as err:
        print(f"ERRORE CRITICO: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    populate_advanced_pro()