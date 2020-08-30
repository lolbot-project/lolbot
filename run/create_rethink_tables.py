from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError

r = RethinkDB()
tables = ["userconfig", "serverconfig"]

conn = r.connect("localhost", 28015)

try:
    r.db_create('lolbot').run(conn)
    print("- Created lolbot db")
except ReqlOpFailedError:
    print("* lolbot DB creation failed. Most likely already exists")
conn.use("lolbot")

for table in tables:
    try:
        r.table_create(table).run(conn)
        print(f"- Created {table} table")
    except ReqlOpFailedError:
        print(f"* {table} table creation failed. Most likely already exists")

print("- Done!")