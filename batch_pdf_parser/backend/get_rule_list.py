#!/usr/bin/python3

import cgi
import json
import mysql.connector

def get_rule_list(field_data):
    try:
        # Declare necessary lists
        rule_list = list()
        
        # Generate SELECT statement
        command = "SELECT rule_name FROM pdf_parser.rules WHERE template_name = '" + str(field_data['template_name'].value) + "'"

        # Execute SELECT statement, reformat results, and handle MySQL errors
        try:
            connection = mysql.connector.connect(user='***', password='***', host='***', port='***')
            cursor = connection.cursor()
            cursor.execute(command)
            results = cursor.fetchall()
        except mysql.connector.Error as mysql_error:
            error_message = 'MySQL Error: ' + str(mysql_error)
            success_message = ''
            return error_message, success_message, rule_list
        
        for row in results:
            for item in row:
                rule_list.append(item)

    # Hanlde Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error) + ' - Error Type: ' + str(type(py_error))
        success_message = ''
        return error_message, success_message, rule_list

    # Return message and rule list if no errors
    error_message = ''
    success_message = ''
    return error_message, success_message, rule_list



def main():
    # Execute main function and return message and rule list to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message, rule_list = get_rule_list(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'rule_list' : rule_list}))