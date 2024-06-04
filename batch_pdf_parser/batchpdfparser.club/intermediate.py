#!/usr/bin/python3

import cgi
import json
import sys
import os
sys.path.append('/home/***/backend')
import access_control

def get_destination():
    # Initialize variables
    destination = ''

    # Retrieve destination from HTTP GET request
    try:
        query_string = os.environ['QUERY_STRING']  # alternatively use cgi.print_environ()
        query = query_string.split('; ')
        for query_item in query:
            key, value = query_item.split('=')
            if key == 'destination':
                destination = value
                break
    except:
        destination = ''
    return destination

# Redirect to public destinations
def public_destination_check(destination):
    if destination == 'login':
        import login
        login.main()
    elif destination == 'redirect':
        import redirect
        redirect.main()
    else: pass

# Redirect to private destinations
def private_destination_check(destination):
    if destination == 'get_template_list':
        import get_template_list
        get_template_list.main()
    elif destination == 'get_rule_list':
        import get_rule_list
        get_rule_list.main()
    elif destination == 'upload':
        import upload
        upload.main()
    elif destination == 'get_pdf_content':
        import get_pdf_content
        get_pdf_content.main()
    elif destination == 'add_template':
        import add_template
        add_template.main()
    elif destination == 'load_template':
        import load_template
        load_template.main()
    elif destination == 'update_template':
        import update_template
        update_template.main()
    elif destination == 'delete_template':
        import delete_template
        delete_template.main()
    elif destination == 'add_rule':
        import add_rule
        add_rule.main()
    elif destination == 'load_rule':
        import load_rule
        load_rule.main()
    elif destination == 'update_rule':
        import update_rule
        update_rule.main()
    elif destination == 'delete_rule':
        import delete_rule
        delete_rule.main()
    elif destination == 'test_parser':
        import test_parser
        test_parser.main()
    elif destination == 'batch_parser':
        import batch_parser
        batch_parser.main()
    elif destination == 'logout':
        import logout
        logout.main()
    else:
        field_data = cgi.FieldStorage() # access field data to prevent response issues
        error_message = 'Invalid destination.'
        success_message = ''
        return error_message, success_message



# Check user's access status and redirect request accordingly
destination = get_destination()
public_destination_check(destination)
if access_control.access_control() == True:
    error_message, success_message = private_destination_check(destination)
else:
    field_data = cgi.FieldStorage() # access field data to prevent response issues
    error_message = 'Access Denied.'
    success_message = ''
print()
print(json.dumps({'error_message' : error_message, 'success_message' : success_message}))