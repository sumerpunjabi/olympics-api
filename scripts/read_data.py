import csv
import mysql.connector
import os


def main():
    files = ["../data/summer.csv", "../data/winter.csv"]
    # password = os.getenv("PASSWORD")

    # Connect to the MySQL server and select the "olympics" database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='AdidasNike1!',
        database="olympics"
    )

    # Open the CSV file and create a CSV reader object
    for file in files:
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Loop through each row of the CSV file and insert it into the normalized tables
            for row in csv_reader:
                print(row['Name'], row['Age'])
                try:
                    # Insert the country data into the countries table
                    country_query = "INSERT IGNORE INTO countries (name, code) VALUES (%s, %s)"
                    country_values = (row['Team'], row['NOC'])
                    mycursor = mydb.cursor()
                    mycursor.execute(country_query, country_values)
                    mydb.commit()

                    # Insert the athlete data into the athletes table
                    athlete_query = "INSERT INTO athletes (name, sex, age, country_id) VALUES (%s, %s, %s, (SELECT id FROM countries WHERE code = %s))"
                    athlete_values = (row['Name'], row['Sex'], row['Age'], row['NOC'])
                    mycursor.execute(athlete_query, athlete_values)
                    mydb.commit()

                    # Insert the sport data into the sports table
                    sport_query = "INSERT IGNORE INTO sports (name) VALUES (%s)"
                    sport_values = (row['Sport'],)
                    mycursor.execute(sport_query, sport_values)
                    mydb.commit()

                    # Insert the event data into the events table
                    event_query = "INSERT INTO events (name, sport_id) VALUES (%s, (SELECT id FROM sports WHERE name = %s))"
                    event_values = (row['Event'], row['Sport'])
                    mycursor.execute(event_query, event_values)
                    mydb.commit()

                    # Insert the game data into the games table
                    game_query = "INSERT IGNORE INTO games (year, season, city) VALUES (%s, %s, %s)"
                    game_values = (row['Year'], row['Season'], row['City'])
                    mycursor.execute(game_query, game_values)
                    mydb.commit()

                    # Insert the medal data into the medals table
                    medal_query = "INSERT INTO medals (athlete_id, event_id, medal, game_id) VALUES ((SELECT id FROM athletes WHERE name = %s), (SELECT id FROM events WHERE name = %s), %s, (SELECT id FROM games WHERE year = %s AND season = %s AND city = %s))"
                    medal_values = (row['Name'], row['Event'], row['Medal'], row['Year'], row['Season'], row['City'])
                    mycursor.execute(medal_query, medal_values)

                except mysql.connector.errors.DataError and mysql.connector.errors.DatabaseError as err:
                    print(err)
                    continue
        mydb.commit()


if __name__ == "__main__":
    main()
