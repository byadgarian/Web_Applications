#!/usr/bin/python3

import mysql.connector

# SHOW function
def mysql_show(table_name):
    # Declare necessary lists
    results = list()

    # Generate and execute SHOW statement and handle MySQL errors
    command = "SHOW COLUMNS FROM pdf_parser." + str(table_name)
    try:
        connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
        cursor = connection.cursor()
        cursor.execute(command)
        results = cursor.fetchall()
    except mysql.connector.Error as mysql_error:
        error_message = 'MySQL Error: ' + str(mysql_error)
        return error_message, results

    # Return status, message, and table headers to caller
    error_message = ''
    return error_message, results

# SELECT function
def mysql_select(table_name, requested_attributes, provided_atrributes):
    # Declare necessary lists
    results = list()

    # Generate SELECT statement
    command = "SELECT "
    for attribute in requested_attributes: command += str(attribute) + ', '
    command = command[:-2]
    command += " FROM pdf_parser." + str(table_name)
    if len(provided_atrributes.items()) != 0:
        command += " WHERE "
        for key, value in provided_atrributes.items(): command += str(key) + " = '" + str(value) + "' AND "
        command = command[:-5]

    # Execute SELECT statement and handle MySQL errors
    try:
        connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
        cursor = connection.cursor()
        cursor.execute(command)
        results = cursor.fetchall()
    except mysql.connector.Error as mysql_error:
        error_message = 'MySQL Error: ' + str(mysql_error)
        return error_message, results

    # Return status, message, and table data to caller
    error_message = ''
    return error_message, results