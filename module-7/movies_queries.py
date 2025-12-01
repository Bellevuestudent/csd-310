# movies_update_and_delete.py
# Patrice Moracchini
# CSD-310 - Module 7.2
# This script connects to a MySQL database and performs four data queries
# to retrieve and display records from the 'studio', 'genre', and 'film' tables.


# import the MySQL Connector/Python module
import mysql.connector
from mysql.connector import errorcode

from dotenv import dotenv_values  # use the .env file

# using our .env file
secrets = dotenv_values(".env")

# database configuration object 
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # not in .env file
}

db = None

try:
    # connect to the MySQL database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # 1) First query: select all fields from the studio table
    
    print(" -- DISPLAYING Studio RECORDS --")

    studio_query = "SELECT studio_id, studio_name FROM studio"
    cursor.execute(studio_query)
    studio_records = cursor.fetchall()

    for studio_id, studio_name in studio_records:
        print(f"Studio ID: {studio_id}")
        print(f"Studio Name: {studio_name}\n")
    
    # 2) Second query: select all fields from the genre table
    print("\n -- DISPLAYING Genre RECORDS --")

    genre_query = "SELECT genre_id, genre_name FROM genre"
    cursor.execute(genre_query)
    genre_records = cursor.fetchall()

    for genre_id, genre_name in genre_records:
        print(f"Genre ID: {genre_id}")
        print(f"Genre Name: {genre_name}\n")

   
    # 3) Third query: movie names with runtime < 120 minutes
    #    (ordered by film_name)

    print("\n -- DISPLAYING Short Film RECORDS --")

    short_film_query = """
        SELECT film_name, film_runtime
        FROM film
        WHERE film_runtime < 120
        ORDER BY film_name
    """
    cursor.execute(short_film_query)
    short_films = cursor.fetchall()

    for film_name, runtime in short_films:
        print(f"Film Name: {film_name}")
        print(f"Runtime: {runtime}\n")

    
    # 4) Fourth query: film names and directors, grouped by director
    #    (Grouped by film_director)
    
    print("\n -- DISPLAYING Director RECORDS in Order --")

    director_query = """
        SELECT film_name, film_director
        FROM film
        ORDER BY film_director
    """
    cursor.execute(director_query)
    director_records = cursor.fetchall()

    for film_name, director in director_records:
        print(f"Film Name: {film_name}")
        print(f"Director: {director}\n")

    cursor.close()
    
# handle potential MySQL errors
except mysql.connector.Error as err:
    """ on error code """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)
        
finally:
    """ close the connection to MySQL """
    if db is not None and db.is_connected():
        db.close()