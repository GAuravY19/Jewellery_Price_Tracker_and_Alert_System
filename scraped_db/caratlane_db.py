import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(host=os.getenv('host'),
                        dbname = os.getenv('dbname_c'),
                        user=os.getenv('user'),
                        password = os.getenv('password'),
                        port=os.getenv('port'))

cur = conn.cursor()

# Bluestone
cur.execute("""CREATE TABLE IF NOT EXISTS rings(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS earrings(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS solitaires(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS nosepins(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS bracelets(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS bangles(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS necklace(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS pendants(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS mangalsutras(
    id VARCHAR PRIMARY KEY,
    product_name VARCHAR(1024),
    date_price VARCHAR(64)
)""")


conn.commit()
cur.close()
conn.close()
