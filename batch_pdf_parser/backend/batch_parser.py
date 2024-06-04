#!/usr/bin/python3

import cgi
import os
import json
import csv
import mysql_select
import pdf_parser   # PDF parser class (not a library)

def batch_parse(field_data):
    try:
        # Declare necessary integers, strings and lists
        pdf_directory = '/home/***/backend/pdf_files/'
        csv_directory = 'csv_files/'    # or '/home/***/***/csv_files/'
        i1 = 0
        download_url = ''
        pdf_data_list = list()

        # Create parser object
        parser = pdf_parser.pdf_parser()

        # Retrieve rules and handle errors
        mysql_error_message, results1 = mysql_select.mysql_select('templates', ['*'], {'template_name' : field_data['template_name'].value})
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, download_url
        mysql_error_message, results2 = mysql_select.mysql_show('templates')
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, download_url
        mysql_error_message, results3 = mysql_select.mysql_select('rules', ['*'], {'template_name' : field_data['template_name'].value})
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, download_url
        mysql_error_message, results4 = mysql_select.mysql_show('rules')
        if mysql_error_message != '':
            error_message = mysql_error_message
            success_message = ''
            return error_message, success_message, download_url
        for i2 in range(0, len(results3)):
            rule = dict()
            for i3 in range(0, len(results4)): rule.update({results4[i3][0] : results3[i2][i3]})
            for i4 in range(0, len(results2)): rule.update({results2[i4][0] : results1[0][i4]})
            parser.rules.append(rule)

        # Send each file to parser for processing and handle errors
        for file_name in os.listdir(pdf_directory):
            if (file_name[len(file_name)-3:] != 'pdf' and file_name[len(file_name)-3:] != 'PDF'): os.remove(pdf_directory + file_name)
        files = os.listdir(pdf_directory)
        if len(files) == 0:
            error_message = 'No PDF files to parse.'
            success_message = ''
            return error_message, success_message, download_url
        for file_name in files:
            single_pdf_data = dict()
            if not os.path.isfile(pdf_directory + file_name) or (file_name[len(file_name)-3:] != 'pdf' and file_name[len(file_name)-3:] != 'PDF'):
                error_message = 'File type not supported.'
                success_message = ''
                return error_message, success_message, download_url
            parser.parse(pdf_directory, file_name)

            # Initialize PO data, update PO data using parser data, and format data as needed
            single_pdf_data.update({'id' : str(int(field_data['optional_id'].value) + i1) if field_data['optional_id'].value else 'NA'})
            single_pdf_data.update({'file_name' : file_name})
            for key, value in parser.pdf_data.items(): single_pdf_data.update({value[0] : value[1]})

            # Store data extracted from each PDF file in a list
            pdf_data_list.append(single_pdf_data)

            # Delete each PDF file, and update counter
            os.remove(pdf_directory + file_name)
            i1 += 1

            # Infinite loop safeguard
            if i1 > 500:
                error_message = 'Loop count exceeded safeguard size of 500.'
                success_message = ''
                return error_message, success_message, download_url

        # Generate output files and remove unnecessary files
        with open(csv_directory + 'pdf_data.csv', 'w') as csv_file:
            csv.DictWriter(csv_file, fieldnames = pdf_data_list[0].keys()).writeheader()
            csv.DictWriter(csv_file, fieldnames = pdf_data_list[0].keys()).writerows(pdf_data_list)
        csv_file.close()

        # Return message and download URL if no errors
        error_message = ''
        success_message = 'PDF files processed successfully.'
        download_url = csv_directory + 'pdf_data.csv'   # or download_url = 'csv_files/pdf_data.csv'
        return error_message, success_message, download_url

    # Handle Python errors
    except Exception as py_error:
        error_message = 'Py Error: ' + str(py_error)
        success_message = ''
        return error_message, success_message, download_url



def main():
    # Execute main function and return message and download URL to front-end
    field_data = cgi.FieldStorage()
    error_message, success_message, download_url = batch_parse(field_data)    # update file directory here
    print()
    print(json.dumps({'error_message' : error_message, 'success_message' : success_message, 'download_url' : download_url}))