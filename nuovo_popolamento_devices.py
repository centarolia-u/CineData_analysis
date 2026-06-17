'''
Introduzione
'''

import mysql.connector
import random

def add_devices_and_link():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="easy22", 
            database="CineData"
        )
        cursor = db.cursor()
        print("Connessione stabilita per l'aggiornamento Devices...")

        # 1. Inserimento Dispositivi
        devices = [
            ('iPhone 15', 'Mobile'),
            ('Samsung Galaxy S23', 'Mobile'),
            ('Web Browser (Chrome)', 'Desktop'),
            ('Web Browser (Safari)', 'Desktop'),
            ('Smart TV LG (WebOS)', 'TV'),
            ('Apple TV 4K', 'TV'),
            ('PlayStation 5', 'Console'),
            ('Xbox Series X', 'Console')
        ]
        
        # Uso IGNORE per evitare errori se lo lanci due volte
        cursor.executemany(
            "INSERT IGNORE INTO Devices (device_name, platform_type) VALUES (%s, %s)", 
            devices
        )
        print("Tabella Devices popolata.")

        # 2. Recuperiamo gli ID dei dispositivi appena inseriti
        cursor.execute("SELECT device_id FROM Devices")
        device_ids = [row[0] for row in cursor.fetchall()]

        # 3. Aggiorniamo la watch_history esistente
        # Assegniamo un dispositivo casuale a ogni visione che ha il device_id ancora a NULL
        cursor.execute("SELECT watch_id FROM watch_history WHERE device_id IS NULL")
        watch_ids = [row[0] for row in cursor.fetchall()]
        
        print(f"Aggiornamento di {len(watch_ids)} sessioni con dispositivi casuali...")
        
        for w_id in watch_ids:
            random_device = random.choice(device_ids)
            cursor.execute(
                "UPDATE watch_history SET device_id = %s WHERE watch_id = %s",
                (random_device, w_id)
            )

        db.commit()
        print("Aggiornamento completato con successo!")

    except mysql.connector.Error as err:
        print(f"Errore: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    add_devices_and_link()