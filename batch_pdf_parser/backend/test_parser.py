#!/usr/bin/python3

import cgi
import os
import json
import mysql_select
import pdf_parser   # PDF parser class (not a library)

def test_parse(field_data):
    try:
        # Create parser object
        parser = pdf_parser.pdf_parser()

        directory = '/home/***/backend/pdf_files/'

        # Retrieve rule and handle errors
        mysql_error_message, results1 = mysql_select.mysql_select('templates', ['*'], {'template_name' : field_data['template_name'].value})
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, parser.pdf_data
        mysql_error_message, results2 = mysql_select.mysql_show('templates')
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, parser.pdf_data
        mysql_error_message, results3 = mysql_select.mysql_select('rules', ['*'], {'template_name' : field_data['template_name'].value, 'rule_name' : field_data['rule_name'].value})
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, parser.pdf_data
        mysql_error_message, results4 = mysql_select.mysql_show('rules')
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, parser.pdf_data
        for i1 in range(0, len(results3)):
            rule = dict()
            for i2 in range(0, len(results4)): rule.update({results4[i2][0] : results3[i1][i2]})
            for i3 in range(0, len(results2)): rule.update({results2[i3][0] : results1[0][i3]})
            parser.rules.append(rule)

        # Send sample file to parser for processing and handle errors
        for file_name in os.listdir(directory):
            if (file_name[len(file_name)-3:] != 'pdf' and file_name[len(file_name)-3:] != 'PDF') or (file_name == 'merged_pdf_files.pdf'): os.remove(directory + file_name)
        files = os.listdir(directory)
        if len(files) == 0:
            error_message = 'No PDF files to test.'
            success_message = ''
            return error_message, success_message, parser.pdf_data
        file_name = files[0]
        if not os.path.isfile(directory + file_name) or (file_name[len(file_name)-3:] != 'pdf' and file_name[len(file_name)-3:] != 'PDF'):
            error_message = 'File type not supported.'
            success_message = ''
            return error_message, success_message, parser.pdf_data
        parser.parse(directory, file_name)

        # Return message and PDF data if no errors
        error_message = ''
        success_message = ''
        return error_message, success_message, parser.pdf_data

    # Handle Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error)
        success_message = ''
        return error_message, success_message, parser.pdf_data



def main():
    # Execute main function and return message and PDF data to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message, pdf_data = test_parse(field_data)
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'pdf_data' : pdf_data}))