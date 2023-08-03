import webbrowser
import subprocess
import os
import sqlite3

print("-----------------------medical-assistant------------------------")
print("Checking if database exists")
if not os.path.exists("./backend/data1.db"):
    print("Database not found. Creating Database")

    conn = sqlite3.connect("./backend/data1.db")

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE "prompts" (
	    "message_id"	INTEGER NOT NULL UNIQUE,
	    "user_id"	INTEGER NOT NULL UNIQUE,
	    "prompt"	TEXT NOT NULL,
	    "response"	TEXT NOT NULL,
	    "created"	INTEGER NOT NULL,
	    FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
	    PRIMARY KEY("message_id" AUTOINCREMENT)
    )""")

    cursor.execute("""CREATE TABLE "users" (
	    "user_id"	INTEGER NOT NULL UNIQUE,
	    "username"	TEXT NOT NULL,
	    "email"	TEXT NOT NULL,
	    "salt"	TEXT NOT NULL,
	    "password_hash"	TEXT NOT NULL,
	    PRIMARY KEY("user_id")
    )""")
    cursor.close()
    print("Finished creating Database")

