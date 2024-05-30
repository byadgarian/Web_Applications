#!/usr/bin/python3

import cgi
import json
import mysql.connector

def update_rule(field_data):
    try:
        # Generate UPDATE statement and handle errors
        command = "UPDATE pdf_parser.rules SET "
        for key in field_data.keys():
            if key == 'destination': continue
            elif key == 'new_rule_name': continue
            elif key == 'rule_name': command += str(key) + " = '" + str(field_data['new_rule_name'].value).replace("\\", "\\\\").replace("'", "\\'") + "', "
            else: command += str(key) + " = '" + str(field_data[key].value).replace("\\", "\\\\").replace("'", "\\'") + "', "
        command = command[:-2]
        command += "WHERE template_name = '" + str(field_data['template_name'].value) + "' AND rule_name = '" + str(field_data['rule_name'].value) + "'"

        # Execute UPDATE statement and handle MySQL errors
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
    success_message = 'Rule updated successfully.'
    return error_message, success_message



def main():
    # Execute main function and return message to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message = update_rule(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message}))