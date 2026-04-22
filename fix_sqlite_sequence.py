import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")
conn = sqlite3.connect(db_path)
c = conn.cursor()

tables = [
    "dashboard_seriegraphique",
    "dashboard_observation",
    "dashboard_graphique",
    "dashboard_thematique",
]

for table in tables:
    c.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table}")
    max_id = c.fetchone()[0]
    c.execute(
        "UPDATE sqlite_sequence SET seq = ? WHERE name = ?",
        (max_id, table),
    )
    print(f"{table} -> seq = {max_id}")

conn.commit()
conn.close()
print("Sequences corrigees.")
