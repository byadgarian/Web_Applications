#!/usr/bin/python3

import os
import mysql.connector

def access_control():
    try:
        # Initialize variables
        client_session_id = None

        # Retrieve user's session_id from HTTP cookie header
        cookies_string = os.environ['HTTP_COOKIE']  # alternatively use cgi.print_environ()
        cookies = cookies_string.split('; ')
        for cookie in cookies:
            key, value = cookie.split('=')
            if key == 'session_id':
                client_session_id = value
                break
        
        # Retrieve user's session_id from database, compare with client session_id, and determine access status
        command = "SELECT * FROM pdf_parser.users WHERE session_id = '" + str(client_session_id) + "'"  # what if client_session_id is null not 0?
        connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
        cursor = connection.cursor()
        cursor.execute(command)
        results = cursor.fetchall()
        
        if len(results) != 0:
            server_session_id = str(results[0][3])
        else: 
            server_session_id = '0'

        if server_session_id == '0':
            access_status = False
        elif client_session_id == server_session_id:
            # check if current time is more than 30 minutes ahead of last activity timestamp
            # if yes, delete session_id and last activity timestamp from users table and retrun False access_status
            # else, update the last activity timestamp and return True access_status
            access_status = True
        else:
            access_status = False

    # Return access status
    except:
        access_status = False

    return access_status