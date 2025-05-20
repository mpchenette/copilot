import mysql.connector

def search_user(username):
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    # Execute the query and process the results
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_user(username, password):
    conn = mysql.connector.connect
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "')"

    # Execute the query
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return True



  
