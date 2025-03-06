import mysql.connector

def search_user(username):
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    
    # Execute the query and process the results
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_user(username, password):
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"

    # Execute the query
    cursor.execute(query, (username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def search_specific_user(username):
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND username REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?!edu$)[a-zA-Z]{2,}$'"
    
    # Execute the query and process the results
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result