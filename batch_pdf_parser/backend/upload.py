#!/usr/bin/python3

import cgi
import json
import os

def upload(field_data):
    try:
        # Initialize variables
        file_count = 0
        directory = '/home/***/backend/pdf_files/'

        # Retrieve files from client
        # try:
        file_items = field_data['pdf_files[]']
        # except:
        #     error_message = 'pdf_files[] not set.'
        #     success_message = ''
        #     return error_message, success_message
        
        # Delete old files from directory
        if len(os.listdir(directory)) != 0:
            for file_name in os.listdir(directory):
                os.remove(directory + file_name)

        # Determine upload type and save files
        try:
            for i0 in range(0, len(file_items)):
                file_name = file_items[i0].filename
                file_content = file_items[i0].file.read()
                file = directory + os.path.basename(file_name)
                open(file, "wb").write(file_content)
                file_count += 1
        except:
            file_count = 1
            file_item = file_items
            file_name = file_item.filename
            file_content = file_item.file.read()
            file = directory + os.path.basename(file_name)
            open(file, "wb").write(file_content)
    
    # Hanlde Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error) + ' - Error Type: ' + str(type(py_error))
        success_message = ''
        return error_message, success_message
    
    # Return message if no errors
    error_message = ''
    success_message = str(file_count) + " PDF file(s) uploaded successfully."
    return error_message, success_message



def main():
    # Execute main function and return message to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message = upload(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message}))