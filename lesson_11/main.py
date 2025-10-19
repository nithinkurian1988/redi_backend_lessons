import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def create_table(conn):
    ''' Create a database table for the drivers '''
    try:
        sql_create_drivers_table = """ CREATE TABLE IF NOT EXISTS drivers (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            location text NOT NULL,
                                            status text NOT NULL
                                        ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_drivers_table)
    except sqlite3.Error as e:
        print(e)

def insert_driver(conn, driver):
    ''' Insert a new driver into the drivers table '''
    sql = ''' INSERT INTO drivers(name,location,status)
              VALUES(?,?,?) '''
    cursor = conn.cursor()
    # check if the driver already exists
    cursor.execute('SELECT * FROM drivers WHERE name=? AND location=?', (driver[0], driver[1]))
    data = cursor.fetchone()
    if data is None:
        cursor.execute(sql, driver)
        conn.commit()
        return cursor.lastrowid 

def find_free_drivers(conn, location):
    ''' Query drivers by location and status '''
    sql = ''' SELECT id, name, location, status FROM drivers
              WHERE location=? AND status='free' '''
    cursor = conn.cursor()
    cursor.execute(sql, (location,))

    rows = cursor.fetchall()
    for row in rows:
        print(row)

def book_driver(conn, driver_id):
    ''' Update driver status to booked '''
    sql = ''' UPDATE drivers
              SET status = 'booked'
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (driver_id,))
    conn.commit()

def remove_driver(conn, driver_id):
    ''' Delete a driver by driver id '''
    sql = 'DELETE FROM drivers WHERE id=?'
    cursor = conn.cursor()
    cursor.execute(sql, (driver_id,))
    conn.commit()

def add_driver_rating(conn, driver_id, rating):
    ''' Add a rating for a driver '''
    sql = ''' CREATE TABLE IF NOT EXISTS ratings (
                  id integer PRIMARY KEY,
                  driver_id integer NOT NULL,
                  rating integer NOT NULL,
                  FOREIGN KEY (driver_id) REFERENCES drivers (id)
              ); '''
    cursor = conn.cursor()
    cursor.execute(sql)

    sql_insert_rating = ''' INSERT INTO ratings(driver_id, rating)
                            VALUES(?,?) '''
    cursor.execute(sql_insert_rating, (driver_id, rating))
    conn.commit()

def find_driver_rating(conn, driver_id):
    ''' Find the average rating for a driver '''
    sql = ''' SELECT rating FROM ratings
              WHERE driver_id=? '''
    cursor = conn.cursor()
    cursor.execute(sql, (driver_id,))
    rows = cursor.fetchall()
    ratings = [row[0] for row in rows]
    if ratings:
        average_rating = sum(ratings) / len(ratings)
        print(f'Average rating for driver {driver_id}: {average_rating}')
    else:
        print(f'No ratings found for driver {driver_id}')

def main():
    database = "drivers.db"

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn)
    else:
        print("Error! cannot create the database connection.")

    # insert drivers
    with conn:
        drivers = [
            ('andrew', 'munich', 'free'),
            ('sophie', 'berlin', 'booked'),
            ('zayn', 'munich', 'booked'),
            ('clara', 'munich', 'free'),
            ('william', 'berlin', 'free')
        ]

        for driver in drivers:
            driver_id = insert_driver(conn, driver)
            if driver_id:
                print(f'Driver added with id: {driver_id}')

    # find free drivers in munich
    print("Free drivers in munich:")
    find_free_drivers(conn, 'munich')

    # Book a driver
    print("Booking driver with id 1")
    book_driver(conn, 1)

    # Add a new driver
    new_driver = ('emma', 'munich', 'free')
    driver_id = insert_driver(conn, new_driver)
    print(f'New driver added with id: {driver_id}')

    # Remove the driver
    print("Removing driver with id 2")
    remove_driver(conn, 2)

    # Add rating for driver
    print("Adding rating 5 for driver with id 3")
    add_driver_rating(conn, 3, 5)

    # Add another rating for driver
    print("Adding rating 4 for driver with id 3")
    add_driver_rating(conn, 3, 4)

    # Find ratings for driver
    print("Ratings for driver with id 3:")
    find_driver_rating(conn, 3)

if __name__ == '__main__':
    main()