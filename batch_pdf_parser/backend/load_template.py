#!/usr/bin/python3

import cgi
import json
import mysql.connector

def load_template(field_data):
    try:
        # Declare necessary dictionaries
        template = dict()

        # Generate SELECT and SHOW statements
        command1 = "SELECT * FROM pdf_parser.templates WHERE template_name = '" + str(field_data['template_name'].value) + "'"
        command2 = "SHOW COLUMNS FROM pdf_parser.templates"

        # Execute SELECT and SHOW statements, merge results, and handle MySQL errors
        try:
            connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
            cursor = connection.cursor()
            cursor.execute(command1)
            results1 = cursor.fetchall()
            cursor.execute(command2)
            results2 = cursor.fetchall()
        except mysql.connector.Error as mysql_error:
            error_message = 'MySQL Error: ' + str(mysql_error)
            success_message = ''
            return error_message, success_message, template
        for i1 in range(0, len(results2)): template.update({results2[i1][0] : results1[0][i1]})

    # Hanlde Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error) + ' - Error Type: ' + str(type(py_error))
        success_message = ''
        return error_message, success_message, template

    # Return message and template data if no errors
    error_message = ''
    success_message = ''
    return error_message, success_message, template



def main():
    # Execute main function and return message and template data to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message, template = load_template(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'template' : template}))