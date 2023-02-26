from fastapi import FastAPI
import mysql.connector

app = FastAPI()

# Connect to the MySQL server and select the "olympics" database
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AdidasNike1!",
    database="olympics"
)


# Endpoint to retrieve all rows from the "athletes" table
@app.get("/athlete")
def get_athletes():
    cursor = cnx.cursor()
    # select a random row from the "athletes" table, join with the other 4 tables, and return the result
    cursor.execute("""
      SELECT
      a.id AS ID,
      a.name AS Name, 
      a.sex AS Sex, 
      a.age AS Age, 
      c.name AS Team, 
      c.code AS NOC, 
      g.year AS Games,
      g.season AS Season, 
      g.city AS City, 
      s.name AS Sport, 
      e.name AS Event, 
      m.medal AS Medal
    FROM 
      athletes a 
      JOIN countries c ON a.country_id = c.id 
      JOIN medals m ON a.id = m.athlete_id 
      JOIN events e ON m.event_id = e.id 
      JOIN games g ON m.game_id = g.id 
      JOIN sports s ON e.sport_id = s.id 
    ORDER BY RAND() 
    LIMIT 1;
    """)
    rows = cursor.fetchall()
    cursor.close()
    dic = to_dict(rows[0])
    return dic


@app.get("/id/{id}")
def get_id(id: int):
    cursor = cnx.cursor()
    cursor.execute("""
    SELECT 
  a.id AS ID,
  a.name AS Name, 
  a.sex AS Sex, 
  a.age AS Age, 
  c.name AS Team, 
  c.code AS NOC, 
  g.year AS Games,
  g.season AS Season, 
  g.city AS City, 
  s.name AS Sport, 
  e.name AS Event, 
  m.medal AS Medal
FROM 
  athletes a 
  JOIN countries c ON a.country_id = c.id 
  JOIN medals m ON a.id = m.athlete_id 
  JOIN events e ON m.event_id = e.id 
  JOIN games g ON m.game_id = g.id 
  JOIN sports s ON e.sport_id = s.id 
WHERE 
  a.id = {};
    """.format(id))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 0:
        return {"error": "Something went Wrong."}
    dic = to_dict(rows[0])
    return dic


@app.get("/sports")
def get_sports():
    cursor = cnx.cursor()
    cursor.execute("""
    SELECT DISTINCT name 
    FROM sports;
    """)
    rows = cursor.fetchall()
    sports = [row[0] for row in rows]
    cursor.close()
    dic = {'sports': sports}
    return dic


@app.get("/events")
def get_events():
    cursor = cnx.cursor()
    cursor.execute("""
    SELECT DISTINCT name 
    FROM events;
    """)
    rows = cursor.fetchall()
    events = [row[0] for row in rows]
    cursor.close()
    dic = {'events': events}
    return dic


# Close the MySQL connection when the application shuts down
@app.on_event("shutdown")
def shutdown():
    cnx.close()


def to_dict(lst):
    dic = {'ID': lst[0], 'Name': lst[1], 'Sex': lst[2], 'Age': lst[3], 'Team': lst[4], 'NOC': lst[5], 'Games': lst[6],
           'Season': lst[7], 'City': lst[8], 'Sport': lst[9], 'Event': lst[10], 'Medal': lst[11]}
    return dic


# Run the FastAPI application using the uvicorn server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
