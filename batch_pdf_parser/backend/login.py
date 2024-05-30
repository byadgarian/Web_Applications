#!/usr/bin/python3

import json
import cgi
import mysql.connector

def login(field_data):
    # Retrieve user's credentials from client
    try:
        client_username = field_data['username'].value
        client_password = field_data['password'].value
    except:
        client_username = None
        client_password = None

    # Retrieve user's credentials from database, compare with client credentials, and assign seesion_id if matched
    command = "SELECT * FROM pdf_parser.users WHERE user_name = '" + str(client_username) + "'"
    try:
        connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
        cursor = connection.cursor()
        cursor.execute(command)
        results = cursor.fetchall()
    except mysql.connector.Error as mysql_error:
        error_message = 'MySQL Error: ' + str(mysql_error)
        success_message = ''
        redirect_url = ''
        client_session_id = None
        return error_message, success_message, redirect_url, client_session_id
    
    if len(results) != 0:
        server_username = results[0][1]
        server_password = results[0][2]

        if client_username == server_username and client_password == server_password:
            session_id = '***'  # generate randomly and make sure it's not in users table already
            error_message = ''
            success_message = ''
            redirect_url = '/'

            # Update user's session_id in the database
            command = "UPDATE pdf_parser.users SET session_id = '" + str(session_id) + "' WHERE user_name = '" + str(server_username) + "'"
            try:
                connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
                cursor = connection.cursor()
                cursor.execute(command)
                connection.commit()
            except mysql.connector.Error as mysql_error:
                error_message = 'MySQL Error: ' + str(mysql_error)
                success_message = ''
                redirect_url = ''
                client_session_id = None
                return error_message, success_message, redirect_url, client_session_id

            client_session_id = session_id
            return error_message, success_message, redirect_url, client_session_id
    
        else:
            error_message = 'Password is incorrect.'
            success_message = ''
            redirect_url = ''
            client_session_id = None
            return error_message, success_message, redirect_url, client_session_id

    else:
        error_message = 'User does not exist.'
        success_message = ''
        redirect_url = ''
        client_session_id = None
        return error_message, success_message, redirect_url, client_session_id



# Authenticate user, add user's session_id to HTTP cookie header, and redirect user
field_data = cgi.FieldStorage()
error_message, success_message, redirect_url, client_session_id = login(field_data)
# print('Status: 302 Found')
# print('Location: /')
if client_session_id:
    print('Set-Cookie: session_id=' + str(client_session_id) + '; max-age=900; path="/";') # domain='***'; increase expiration time
print()
print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'redirect_url' : redirect_url}))