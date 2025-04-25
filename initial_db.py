import sqlite3


def main():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query_1 = '''
    CREATE TABLE IF NOT EXISTS statistic(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        chat INTEGER,
        date_query TEXT
    );
    '''
    query_2 = '''
    CREATE TABLE IF NOT EXISTS cities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        lat FLOAT,
        lon FLOAT
    );
    '''
    query_3 = '''
    CREATE TABLE IF NOT EXISTS current_city(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat INTEGER,
        city TEXT
    );
    '''
    query_4 = '''
    INSERT INTO cities(name, lat, lon) VALUES (?, ?, ?);
    '''
    cur.execute(query_1)
    cur.execute(query_2)
    cur.execute(query_3)
    cur.execute(query_4, ('Moscow', 55.7522, 37.6156))
    con.commit()
    con.close() 


if __name__ == '__main__':
    main()
