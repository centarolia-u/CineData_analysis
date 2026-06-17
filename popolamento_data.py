'''
Intestazione
'''

import mysql.connector
from faker import Faker
import random

fake = Faker()

def populate_data():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="easy22", 
            database="CineData" # Assicurati di aver prima ricreato il DB
        )
        cursor = db.cursor()
        print("Connessione stabilita con CineData...")

        # 1. Piani
        plans = [('Basic', 7.99, '720p'), ('Standard', 12.99, '1080p'), ('Premium', 17.99, '4K')]
        cursor.executemany("INSERT INTO subscription_plans (plan_name, monthly_price, max_resolution) VALUES (%s, %s, %s)", plans)

        # 2. Generi 
        genres_list = [('Sci-Fi',), ('Drama',), ('Action',), ('Thriller',), ('Crime',), ('Comedy',), ('Horror',), ('Romance',), ('Documentary',), ('Fantasy',)]
        cursor.executemany("INSERT INTO genres (genre_name) VALUES (%s)", genres_list)

        # 3. Film (500)
        print("Sto generando 500 film. Un attimo di pazienza...")
        movies_data = []
        for _ in range(500):
            # Usiamo metodi faker per far finta che siano titoli di film e registi veritieri
            # Limito il testo a 255 caratteri per sicurezza
            title = fake.catch_phrase()[:255] 
            director = fake.name()
            release_year = random.randint(1980, 2024)
            duration_min = random.randint(80, 200)
            rating_score = round(random.uniform(4.0, 9.9), 1)
            movies_data.append((title, director, release_year, duration_min, rating_score))
            
        cursor.executemany("INSERT INTO movies (title, director, release_year, duration_min, rating_score) VALUES (%s, %s, %s, %s, %s)", movies_data)

        # Recuperiamo tutti gli id film e id generi appena generati
        cursor.execute("SELECT movie_id FROM movies")
        movie_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT genre_id FROM genres")
        genre_ids = [row[0] for row in cursor.fetchall()]

        # 4. Associazione Film-Generi (Random da 1 a 3 generi per film)
        movie_genres_associations = []
        for m_id in movie_ids:
            num_genres = random.randint(1, 3)
            selected_genres = random.sample(genre_ids, num_genres)
            for g_id in selected_genres:
                movie_genres_associations.append((m_id, g_id))
                
        cursor.executemany("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", movie_genres_associations)
        print("500 film e categorie generati con successo!")

        # 5. Utenti e Abbonamenti (300)
        print("Sto generando 300 utenti ed abbonamenti (metodo Bulk Insert)...")
        users_data = []
        for _ in range(300):
            reg_date = fake.date_between(start_date='-2y', end_date='today')
            country = random.choice(['Italy', 'USA', 'France', 'Spain', 'Germany', 'UK', 'Japan'])
            users_data.append((fake.first_name(), fake.last_name(), fake.unique.email(), country, reg_date))
            
        cursor.executemany("INSERT INTO users (first_name, last_name, email, country, registration_date) VALUES (%s, %s, %s, %s, %s)", users_data)
        
        # Recupero i dati per associare gli abbonamenti
        cursor.execute("SELECT user_id, registration_date FROM users")
        users = cursor.fetchall()
        
        subscriptions_data = []
        for user_id, reg_date in users:
            plan_id = random.randint(1, 3)
            # Più probabile che un piano sia attivo (trucchetto per avere buoni dati aziendali)
            status = random.choice(['Active', 'Active', 'Active', 'Cancelled', 'Expired']) 
            subscriptions_data.append((user_id, plan_id, reg_date, status))
            
        cursor.executemany("INSERT INTO subscriptions (user_id, plan_id, start_date, status) VALUES (%s, %s, %s, %s)", subscriptions_data)
        db.commit() 

        # 6. Visioni (Watch History)
        print("Sto popolando decine di migliaia di visioni degli utenti (Bulk mode on 🔥)...")
        watch_history_data = []
        
        for user_id, reg_date in users:
            # Tra 15 e 70 visioni per singolo utente
            for _ in range(random.randint(15, 70)):
                movie_id = random.choice(movie_ids)
                watch_date = fake.date_time_between(start_date=reg_date, end_date='now')
                minutes = random.randint(5, 200)
                completed = 1 if minutes > 120 else 0
                
                watch_history_data.append((user_id, movie_id, watch_date, minutes, completed))

        # Qui usiamo di nuovo l'inserimento in blocco per tutto watch_history!
        cursor.executemany("INSERT INTO watch_history (user_id, movie_id, watch_date, minutes_watched, completed) VALUES (%s, %s, %s, %s, %s)", watch_history_data)

        db.commit()
        print(f"Tutto completato! 🚀 Inserite la bellezza di {len(watch_history_data)} storico visioni interamente generate in svariati secondi.")

    except mysql.connector.Error as err:
        print(f"Errore critico MySQL: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    populate_data()