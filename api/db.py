import psycopg2
import psycopg2.extras

config = {
    "user": "postgres",
    "password": "2105",
    "host": "localhost"
}
conn = psycopg2.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    dbname="newsdb"
)



def getarticles(page, limit):
    offset = int(page) * int(limit)
    curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        curr.execute("""SELECT id, link, title, content, created, sentiment, department FROM articles LIMIT %s OFFSET %s;""", (int(limit), int(offset)))
    except psycopg2.Error:
        return []
    data = curr.fetchall()
    curr.close()

    return data

def get_id(id):
    curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        curr.execute("""SELECT id, link, title, content, created, sentiment, department FROM articles WHERE id=%s;""", (id))
    except psycopg2.Error:
        return []
    data = curr.fetchone()
    curr.close()

    return data