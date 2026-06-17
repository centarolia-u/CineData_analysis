'''
Intestazione
'''

import mysql.connector
from mysql.connector import errorcode
import random

# CONFIGURAZIONE (Stessi dati dei tuoi file)
config = {
    'user': 'root', 
    'password': 'easy22', 
    'host': 'localhost',
    'database': 'CineData'
}

def upgrade_database():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        print("Connessione stabilita. Inizio aggiornamento senza perdita dati...")

        # --- 1. CREAZIONE TABELLA DEVICES ---
        sql_devices = (
            "CREATE TABLE IF NOT EXISTS `Devices` ("
            "  `device_id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `device_name` varchar(50) NOT NULL,"
            "  PRIMARY KEY (`device_id`)"
            ") ENGINE=InnoDB")
        
        cursor.execute(sql_devices)
        print("Tabella 'Devices' pronta.")

        # --- 2. AGGIORNAMENTO WATCH_HISTORY (Aggiunta colonna device_id) ---
        # Verifichiamo prima se la colonna esiste già per evitare errori
        cursor.execute("SHOW COLUMNS FROM Watch_History LIKE 'device_id'")
        result = cursor.fetchone()
        
        if not result:
            print("Aggiunta colonna 'device_id' a Watch_History...")
            cursor.execute("ALTER TABLE Watch_History ADD COLUMN device_id int(11)")
            cursor.execute("ALTER TABLE Watch_History ADD FOREIGN KEY (device_id) REFERENCES Devices(device_id)")
        else:
            print("Colonna 'device_id' già presente.")

        # --- 3. POPOLAMENTO DEVICES ---
        # Controlliamo se ci sono già device per non duplicarli
        cursor.execute("SELECT COUNT(*) FROM Devices")
        if cursor.fetchone()[0] == 0:
            device_list = [('Smart TV',), ('Smartphone',), ('Tablet',), ('Web Browser',), ('Game Console',)]
            cursor.executemany("INSERT INTO Devices (device_name) VALUES (%s)", device_list)
            print("Tipi di device inseriti.")
        
        # Recuperiamo gli ID dei nuovi device
        cursor.execute("SELECT device_id FROM Devices")
        ids_device = [row[0] for row in cursor.fetchall()]

        # --- 4. ASSEGNAZIONE RETROATTIVA (Il tocco magico) ---
        # Assegniamo un device random a tutte le visioni che hanno ancora il device_id NULL
        print("Assegnazione device casuali alle visioni esistenti...")
        cursor.execute("SELECT watch_id FROM Watch_History WHERE device_id IS NULL")
        visioni_da_aggiornare = cursor.fetchall()

        if visioni_da_aggiornare:
            updates = []
            for (w_id,) in visioni_da_aggiornare:
                updates.append((random.choice(ids_device), w_id))
            
            # Usiamo executemany per essere veloci
            cursor.executemany("UPDATE Watch_History SET device_id = %s WHERE watch_id = %s", updates)
            print(f"Aggiornate {len(updates)} visioni con dati sui dispositivi!")
        else:
            print("Tutte le visioni hanno già un device associato.")

        cnx.commit()
        print("\nSUCCESS! Il database è stato arricchito senza cancellare nulla.")
        print("Ora su Power BI ti basterà cliccare su 'Aggiorna' per vedere la nuova tabella e i nuovi dati.")

    except mysql.connector.Error as err:
        print(f"Errore durante l'upgrade: {err}")
    finally:
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()

if __name__ == "__main__":
    upgrade_database()