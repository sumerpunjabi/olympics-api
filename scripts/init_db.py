import mysql.connector
import os


# Script to initialize the database, run once to create the database and tables
def initDB():
    password = os.getenv("PASSWORD")

    # Connect to MySQL server
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password
    )

    # Create the "olympics" database
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS olympics")
    cnx.database = "olympics"

    # Create the "countries" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            code VARCHAR(3) NOT NULL,
            PRIMARY KEY (id)
        )
    """)

    # Create the "athletes" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS athletes (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            sex VARCHAR(10) NOT NULL,
            age INT NOT NULL,
            country_id INT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    """)

    # Create the "sports" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sports (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
    """)

    # Create the "events" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INT NOT NULL AUTO_INCREMENT,
            sport_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (sport_id) REFERENCES sports(id)
        )
    """)

    # Create the "games" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INT NOT NULL AUTO_INCREMENT,
            year INT NOT NULL,
            season VARCHAR(10) NOT NULL,
            city VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        )
    """)

    # Create the "medals" table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medals (
            id INT NOT NULL AUTO_INCREMENT,
            athlete_id INT NOT NULL,
            event_id INT NOT NULL,
            medal VARCHAR(255),
            game_id INT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (athlete_id) REFERENCES athletes(id),
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (game_id) REFERENCES games(id)
        )
    """)

    # Close the cursor and connection
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    initDB()
