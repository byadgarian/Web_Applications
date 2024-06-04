#!/usr/bin/python3

import cgi
import json
import mysql.connector

def add_template(field_data):
    try:
        # Generate INSERT statement and handle errors
        command = "INSERT INTO pdf_parser.templates ("
        for key in field_data.keys():
            if key == 'destination': continue
            else: command += str(field_data[key].name) + ", "
        command = command[:-2]
        command += ") VALUES ('"
        for key in field_data.keys():
            if key == 'destination': continue
            else: command += str(field_data[key].value).replace("\\", "\\\\").replace("'", "\\'") + "', '"
        command = command[:-3]
        command += ")"

        # Execute INSERT statement and handle MySQL errors
        try:
            connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
        except mysql.connector.Error as mysql_error:
            error_message = 'MySQL Error: ' + str(mysql_error)
            success_message = ''
            return error_message, success_message

    # Hanlde Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error) + ' - Error Type: ' + str(type(py_error))
        success_message = ''
        return error_message, success_message

    # Return message if no errors
    error_message = ''
    success_message = 'Template added successfully.'
    return error_message, success_message



def main():
    # Execute main function and return message to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message = add_template(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message}))