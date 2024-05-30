#!/usr/bin/python3

import os
import json
import mysql.connector

def logout():
    try:
        # Initialize variables
        session_id = None

        # Retrieve user's session_id from HTTP cookie header
        cookies_string = os.environ['HTTP_COOKIE']  # alternatively use cgi.print_environ()
        cookies = cookies_string.split('; ')
        for cookie in cookies:
            key, value = cookie.split('=')
            if key == 'session_id':
                session_id = value
                break

        # Revoke user's session_id in database
        command = "UPDATE pdf_parser.users SET session_id = '0' WHERE session_id = '" + str(session_id) + "'"   # what if session_id is null?
        try:
            connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
            error_message = ''
            success_message = ''
            redirect_url = '/'
            return error_message, success_message, redirect_url
        except mysql.connector.Error as mysql_error:
            error_message = 'MySQL Error: ' + str(mysql_error)
            success_message = ''
            redirect_url = ''
            return error_message, success_message, redirect_url

    except:
        error_message = 'Logout failed.'
        success_message = ''
        redirect_url = ''
        return error_message, success_message, redirect_url



def main():
    # Log user out, clear user's session_id from HTTP cookie header, and redirect user
    error_message, success_message, redirect_url = logout()
    print('Set-Cookie: session_id=' + '' + '; max-age=0; path="/";') # should session_id be null or 0?
    # print('Status: 302 Found')
    # print('Location: /')
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'redirect_url' : redirect_url}))