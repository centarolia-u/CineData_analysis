'''
Intestazione
'''

import mysql.connector
from mysql.connector import errorcode

# Configurazione della connessione
config = {
    'user': 'root', # Il tuo username di Workbench
    'password': 'easy22', # La tua password
    'host': 'localhost',
}

TABLES = {}

TABLES['Subscription_Plans'] = (
    "CREATE TABLE `Subscription_Plans` ("
    "  `plan_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `plan_name` varchar(50) NOT NULL,"
    "  `monthly_price` decimal(5,2) NOT NULL,"
    "  `max_resolution` varchar(10),"
    "  PRIMARY KEY (`plan_id`)"
    ") ENGINE=InnoDB")

TABLES['Users'] = (
    "CREATE TABLE `Users` ("
    "  `user_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `first_name` varchar(50),"
    "  `last_name` varchar(50),"
    "  `email` varchar(100) UNIQUE,"
    "  `country` varchar(50),"
    "  `registration_date` date,"
    "  PRIMARY KEY (`user_id`)"
    ") ENGINE=InnoDB")

TABLES['Genres'] = (
    "CREATE TABLE `Genres` ("
    "  `genre_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `genre_name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`genre_id`)"
    ") ENGINE=InnoDB")

TABLES['Movies'] = (
    "CREATE TABLE `Movies` ("
    "  `movie_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `title` varchar(255) NOT NULL,"
    "  `director` varchar(100),"
    "  `release_year` int(11),"
    "  `duration_min` int(11),"
    "  `rating_score` decimal(3,1),"
    "  PRIMARY KEY (`movie_id`)"
    ") ENGINE=InnoDB")

TABLES['Subscriptions'] = (
    "CREATE TABLE `Subscriptions` ("
    "  `sub_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `user_id` int(11),"
    "  `plan_id` int(11),"
    "  `start_date` date,"
    "  `status` enum('Active', 'Expired', 'Cancelled'),"
    "  PRIMARY KEY (`sub_id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`),"
    "  FOREIGN KEY (`plan_id`) REFERENCES `Subscription_Plans` (`plan_id`)"
    ") ENGINE=InnoDB")

TABLES['Movie_Genres'] = (
    "CREATE TABLE `Movie_Genres` ("
    "  `movie_id` int(11),"
    "  `genre_id` int(11),"
    "  PRIMARY KEY (`movie_id`, `genre_id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `Movies` (`movie_id`),"
    "  FOREIGN KEY (`genre_id`) REFERENCES `Genres` (`genre_id`)"
    ") ENGINE=InnoDB")

# ECCO LA TABELLA CHE MANCAVA!
TABLES['Watch_History'] = (
    "CREATE TABLE `Watch_History` ("
    "  `watch_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `user_id` int(11),"
    "  `movie_id` int(11),"
    "  `watch_date` datetime,"
    "  `minutes_watched` int(11),"
    "  `completed` tinyint(1),"
    "  PRIMARY KEY (`watch_id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `Movies` (`movie_id`)"
    ") ENGINE=InnoDB")

TABLES['Dim_Calendar'] = (
    "CREATE TABLE `Dim_Calendar` ("
    "  `date_id` date NOT NULL,"
    "  `year` int NOT NULL,"
    "  `month` int NOT NULL,"
    "  `month_name` varchar(20),"
    "  `day` int NOT NULL,"
    "  `day_of_week` varchar(20),"
    "  `is_weekend` tinyint(1),"
    "  `quarter` int NOT NULL,"
    "  PRIMARY KEY (`date_id`)"
    ") ENGINE=InnoDB")

TABLES['Reviews'] = (
    "CREATE TABLE `Reviews` ("
    "  `review_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `user_id` int(11),"
    "  `movie_id` int(11),"
    "  `rating` int(1) CHECK (rating >= 1 AND rating <= 5),"
    "  `comment` text,"
    "  `review_date` date,"
    "  PRIMARY KEY (`review_id`),"
    "  FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`),"
    "  FOREIGN KEY (`movie_id`) REFERENCES `Movies` (`movie_id`)"
    ") ENGINE=InnoDB")

def create_database():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS CineData DEFAULT CHARACTER SET 'utf8'")
        print("Database 'CineData' pronto.")
        
        cursor.execute("USE CineData")

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print(f"Creazione tabella {table_name}: ", end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("già esistente.")
                else:
                    print(err.msg)
            else:
                print("OK")

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Errore: {err}")

if __name__ == "__main__":
    create_database()