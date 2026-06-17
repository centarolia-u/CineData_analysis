'''
Intestazione
'''
'''
import mysql.connector

config = {
    'user': 'root', 
    'password': 'easy22', # La tua password
    'host': 'localhost',
    'database': 'CineData'
}

def fix_reviews_table():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        print("Allineamento tabella 'reviews' in corso...")

        # 1. Eliminiamo la vecchia tabella per evitare conflitti di colonne
        cursor.execute("DROP TABLE IF EXISTS reviews")
        
        # 2. Creiamo la tabella con i campi corretti che il tuo script "avanzato" si aspetta
        # Nota bene: il campo deve chiamarsi proprio 'review_text'
        create_reviews_sql = """
        CREATE TABLE reviews (
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            movie_id INT,
            rating_score DECIMAL(3,1),
            review_text TEXT,
            review_date DATE,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
        ) ENGINE=InnoDB
        """
        cursor.execute(create_reviews_sql)
        
        cnx.commit()
        print("SUCCESS: Tabella 'reviews' ricreata correttamente con la colonna 'review_text'!")

    except mysql.connector.Error as err:
        print(f"Errore: {err}")
    finally:
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()

if __name__ == "__main__":
    fix_reviews_table()
'''

import mysql.connector
from faker import Faker
import random

# CONFIGURAZIONE (usa le tue credenziali)
config = {
    'user': 'root',
    'password': 'easy22',
    'host': 'localhost',
    'database': 'CineData'
}

fake = Faker()

def fix_and_populate_reviews():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        print("Connessione stabilita. Inizio allineamento schema...")

        # 1. ELIMINIAMO LA VECCHIA TABELLA (Per evitare il bug del IF NOT EXISTS)
        # Proviamo a cancellare sia 'reviews' che 'User_Reviews' per pulizia
        cursor.execute("DROP TABLE IF EXISTS reviews")
        cursor.execute("DROP TABLE IF EXISTS User_Reviews")
        print("Vecchi conflitti rimossi.")

        # 2. CREAZIONE TABELLA DEFINITIVA (Standard Professionale)
        cursor.execute("""
            CREATE TABLE reviews (
                review_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                movie_id INT,
                rating INT,
                review_text TEXT,
                review_date DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
            ) ENGINE=InnoDB
        """)
        print("Tabella 'reviews' creata con schema corretto.")

        # 3. RECUPERO ID PER IL POPOLAMENTO
        cursor.execute("SELECT user_id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT movie_id FROM Movies")
        movie_ids = [row[0] for row in cursor.fetchall()]

        # 4. GENERAZIONE DATI
        reviews_data = []
        print(f"Generazione di 1000 recensioni per {len(user_ids)} utenti su {len(movie_ids)} film...")
        
        for _ in range(1000):
            uid = random.choice(user_ids)
            mid = random.choice(movie_ids)
            rating = random.randint(1, 5)
            
            # Testi realistici
            if rating >= 4:
                text = random.choice(["Capolavoro!", "Da vedere assolutamente.", "Regia incredibile.", "Uno dei miei preferiti."])
            elif rating <= 2:
                text = random.choice(["Delusione totale.", "Non lo finirei mai.", "Pessimo montaggio.", "Tempo sprecato."])
            else:
                text = random.choice(["Non male, ma lento.", "Bravi gli attori, meno la storia.", "Pellicola interessante.", "Si può guardare."])
            
            r_date = fake.date_between(start_date='-1y', end_date='today')
            reviews_data.append((uid, mid, rating, text, r_date))

        # 5. INSERT
        query = "INSERT INTO reviews (user_id, movie_id, rating, review_text, review_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(query, reviews_data)
        
        db.commit()
        print(f"SUCCESS! Tabella allineata e {cursor.rowcount} recensioni inserite.")

    except mysql.connector.Error as err:
        print(f"ERRORE CRITICO: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    fix_and_populate_reviews()