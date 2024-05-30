#!/usr/bin/python3

import json
import mysql.connector

def get_template_list():
    try:
        # Declare necessary lists
        template_list = list()

        # Generate SELECT statement
        command = "SELECT template_name FROM pdf_parser.templates"

        # Execute SELECT statement, reformat results, and handle MySQL errors
        try:
            connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
            cursor = connection.cursor()
            cursor.execute(command)
            results = cursor.fetchall()
        except mysql.connector.Error as mysql_error:
            error_message = 'MySQL Error: ' + str(mysql_error)
            success_message = ''
            return error_message, success_message, template_list
        
        for row in results:
            for item in row:
                template_list.append(item)

    # Hanlde Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error) + ' - Error Type: ' + str(type(py_error))
        success_message = ''
        return error_message, success_message, template_list

    # Return message and template list if no errors
    error_message = ''
    success_message = ''
    return error_message, success_message, template_list



def main():
    # Execute main function and return message and template list to front-end
    error_message, success_message, template_list = get_template_list()
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'template_list' : template_list}))