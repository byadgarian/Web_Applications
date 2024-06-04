#!/usr/bin/python3

import cgi
import json
import mysql.connector

def update_template(field_data):
    try:
        # Generate UPDATE statement and handle errors
        command = "UPDATE pdf_parser.templates SET "
        for key in field_data.keys():
            if key == 'new_template_name': continue
            elif key == 'destination': continue
            elif key == 'template_name': command += "template_name = '" + str(field_data['new_template_name'].value).replace("\\", "\\\\").replace("'", "\\'") + "', "
            else: command += str(key) + " = '" + str(field_data[key].value).replace("\\", "\\\\").replace("'", "\\'") + "', "
        command = command[:-2]
        command += "WHERE template_name = '" + str(field_data['template_name'].value) + "'"

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

    # Return and message if no errors
    error_message = ''
    success_message = 'Template updated successfully.'
    return error_message, success_message



def main():
    # Execute main function and return message to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message = update_template(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message}))