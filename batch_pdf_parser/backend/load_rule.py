#!/usr/bin/python3

import cgi
import json
import mysql.connector

def load_rule(field_data):
    try:
        # Declare necessary dictionaries
        rule = dict()

        # Generate SELECT and SHOW statements
        command1 = "SELECT * FROM pdf_parser.rules WHERE template_name = '" + str(field_data['template_name'].value) + "' AND rule_name = '" + str(field_data['rule_name'].value) + "'"
        command2 = "SHOW COLUMNS FROM pdf_parser.rules"

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
            return error_message, success_message, rule
        for i1 in range(0, len(results2)): rule.update({results2[i1][0] : results1[0][i1]})

    # Hanlde Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error) + ' - Error Type: ' + str(type(py_error))
        success_message = ''
        return error_message, success_message, rule

    # Return message and rule data if no errors
    error_message = ''
    success_message = ''
    return error_message, success_message, rule



def main():
    # Execute main function and return message and rule data to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message, rule = load_rule(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'rule' : rule}))