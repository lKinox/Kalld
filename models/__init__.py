import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, username, password):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        connection.close()
        return user is not None
    
class NewUser:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def validate_username(username):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        connection.close()
        return user is None
    
    def validate_email(email):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        connection.close()
        return user is None

    def register(self):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (self.username, self.email, self.password))
        connection.commit()
        connection.close()
        return True
    
