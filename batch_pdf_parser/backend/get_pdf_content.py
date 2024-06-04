#!/usr/bin/python3

import os
import json
import pdfminer.high_level

def get_pdf_content():
    try:
        # Declare necessary dictionaries and strings
        pdf_data = dict()
        directory = '/home/***/backend/pdf_files/'

        # Extract raw PDF file content and handle errors
        if len(os.listdir(directory)) == 0:
            error_message = 'Upload a sample PDF file to see raw content.'
            success_message = ''
            pdf_data.update({'pdf_content' : ''})
            return error_message, success_message, pdf_data
        else:
            error_message = ''
            success_message = ''
            pdf_data.update({'pdf_content' : pdfminer.high_level.extract_text(directory + os.listdir(directory)[0])})
            return error_message, success_message, pdf_data
    
    # Hanlde Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error) + ' - Error Type: ' + str(type(py_error))
        success_message = ''
        return error_message, success_message, pdf_data



def main():
    # Execute main function and return message and PDF data to front-end
    error_message, success_message, pdf_data = get_pdf_content()  # update file directory here
    print('Cache-Control: no-cache')
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'pdf_data' : pdf_data}))