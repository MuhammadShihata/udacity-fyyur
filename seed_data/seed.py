import psycopg2

con = psycopg2.connect("dbname=fyyur user=postgres password=postgres")

cur = con.cursor()

cur.execute('''
    COPY artists(id, name, genres, city, state, phone, website, facebook_link, seeking_venue, seeking_description, image_link)
    FROM '/mnt/e/code/udacity-fyyur/seed_data/artists.csv' 
    DELIMITER ',' 
    CSV HEADER;
''')

cur.execute('''
    COPY venues(id, name, genres, address, city, state, phone, website, facebook_link, seeking_talent, seeking_description, image_link)
    FROM '/mnt/e/code/udacity-fyyur/seed_data/venues.csv' 
    DELIMITER ',' 
    CSV HEADER;
''')

cur.execute('''
    COPY shows(venue_id, artist_id, start_time)
    FROM '/mnt/e/code/udacity-fyyur/seed_data/shows.csv' 
    DELIMITER ',' 
    CSV HEADER;
''')

con.commit()
con.close()
cur.close()

