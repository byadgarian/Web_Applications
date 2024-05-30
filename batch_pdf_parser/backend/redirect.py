#!/usr/bin/python3

import json
import access_control

def redirect():
    # Intialize variables
    index_file_content = ''
    redirect_url = '/login.html'

    # Determine redirect URL based on access status
    if access_control.access_control() == True:
        index_file = open('/home/***/backend/index.html', 'r')
        index_file_content = index_file.read()
        redirect_url = ''
    return index_file_content, redirect_url



# Redirect user
index_file_content, redirect_url = redirect()
print()
print(json.dumps({'index_file_content' : index_file_content, 'redirect_url' : redirect_url}))