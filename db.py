from flask import Flask
import sqlite3


#CREATE USERS DB
#connection = sqlite3.connect("users.db")
#cursor = connection.cursor()
#cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
#cursor.execute("INSERT INTO users (username, email, password) VALUES ('admin', 'devs@nl.bizemailhost.com', 'admin1234')")
#connection.commit()
#connection.close()

#CREATE SMS REPORTS DB
#connection = sqlite3.connect("sms_campaigns.db")
#cursor = connection.cursor()
#cursor.execute("""
#CREATE TABLE IF NOT EXISTS campaigns (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    send_date TEXT,
#    sender_number TEXT,
#    number_count TEXT,
#    finish_date_time TEXT
#)
#""")
#connection.commit()
#connection.close()

#CREATE SMS WEBGHOOKS DB
#connection = sqlite3.connect("webhooks.db")
#cursor = connection.cursor()
#cursor.execute("CREATE TABLE IF NOT EXISTS webhooks (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
#connection.commit()
#connection.close()

#DELETE ALL SMS WEBHOOKS
#connection = sqlite3.connect("webhooks.db")
#cursor = connection.cursor()
#cursor.execute("DELETE FROM webhooks")
#connection.commit()
#connection.close()

#CREATE CALL WEBHOOKS DB
connection = sqlite3.connect("webhooks-call.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS webhooks (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)")
connection.commit()
connection.close()