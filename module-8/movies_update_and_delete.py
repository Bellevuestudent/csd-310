# Patrice Moracchini
# CSD-310 - Module 8.2
# This script inserts, updates, and deletes records in the movies database
# and displays selected fields from the film table after each step.

# import mysql.connector module
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


# Function to display films
def show_films(cursor, title):
    # method to execute an inner join on all tables,
    # iterate over the dataset and output the results to the terminal window.

    # inner join query
    cursor.execute(
        "SELECT film_name AS Name, "
        "       film_director AS Director, "
        "       genre_name AS Genre, "
        "       studio_name AS 'Studio Name' "
        "FROM film "
        "INNER JOIN genre  ON film.genre_id  = genre.genre_id "
        "INNER JOIN studio ON film.studio_id = studio.studio_id"
    )

    # get the results from the cursor object
    films = cursor.fetchall()

    print("\n  -- {} --".format(title))

    # iterate over the film data set and display the results
    for film in films:
        print(
            "Film Name: {}\n"
            "Director: {}\n"
            "Genre Name ID: {}\n"
            "Studio Name: {}\n"
            .format(film[0], film[1], film[2], film[3])
        )

# main method
def main():
    # connect to the database
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # 1) Display original films
        show_films(cursor, "DISPLAYING FILMS")

        # 2) Insert a new film (The Invisible Man)
        # SQL query to insert a new film separately from the data
        # and avoid SQL injection
        insert_film = (
            "INSERT INTO film "
            "(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        # data to insert a new film (can be reused for multiple inserts if needed)
        new_film = ("The Invisible Man", 2020, 124, "Leigh Whannell", 2, 2)
        cursor.execute(insert_film, new_film)
        db.commit()
        
        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # 3) Update Alien as a Horror film
        update_alien = (
            "UPDATE film "
            "SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror') "
            "WHERE film_name = 'Alien'"
        )
        cursor.execute(update_alien)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

        # 4) Delete Gladiator
        delete_gladiator = "DELETE FROM film WHERE film_name = 'Gladiator'"
        cursor.execute(delete_gladiator)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER DELETE")
    
    # handling potential MySQL errors
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password are invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist")
        else:
            print(err)
    finally:
        try:
            db.close()
        except NameError:
            pass

# entry point
if __name__ == "__main__":
    main()