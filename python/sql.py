import mysql.connector

def search_user(username):
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_user(username, password):
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"

    cursor.execute(query, (username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return True
