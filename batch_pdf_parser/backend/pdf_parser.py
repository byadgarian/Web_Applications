#!/usr/bin/python3

import re
import pdfminer.high_level

# PDF parser class
class pdf_parser:
    # Constructor
    def __init__(self):
        # Declare necessary lists and dictionaries
        self.rules = list()
        self.pdf_data = dict()

    # Helper function
    def find_match(self, string_formats, string, location, string_occurrence):
        match = re.findall(string_formats, string)
        if location == 2 and string_occurrence == 0: return match[0]
        elif location == 2 and string_occurrence >= 1 and string_occurrence <= len(match): return match[len(match) - string_occurrence]
        elif location == 2 and string_occurrence <= -1 and abs(string_occurrence) < len(match): return match[abs(string_occurrence)]
        elif location != 2 and string_occurrence == 0 and len(match) != 0: return match[-1]
        elif location != 2 and string_occurrence >= 1 and string_occurrence <= len(match): return match[string_occurrence - 1]
        elif location != 2 and string_occurrence <= -1 and abs(string_occurrence) < len(match): return match[len(match) - 1 - abs(string_occurrence)]
        else: return 'NA'

    # Main function
    def parse(self, directory, file_name):
        # Extract raw PDF file content
        pdf_content = pdfminer.high_level.extract_text(directory + file_name)

        # Search for a match for each rule and add results to a list
        for rule in self.rules:
            keyword_location = None
            if rule['rule_name'] != '' and rule['csv_column_name'] != '' and rule['location'] != '' and rule['string_occurrence'] != '' and rule['string_formats'] != '':
                if rule['keyword'] != '' and rule['keyword_occurrence'] != '':
                    matches = re.finditer(rule['keyword'], pdf_content)
                    i = 1
                    for keyword_match in matches:
                        if i == int(rule['keyword_occurrence']): keyword_location = keyword_match.start()
                        i += 1
                
                # Search entire document
                if int(rule['location']) == 0:
                    start_location = 0
                    end_location = len(pdf_content) - 1
                # Search after a keyword
                elif int(rule['location']) == 1:
                    start_location = keyword_location + len(rule['keyword']) if keyword_location != None else len(pdf_content) - 1
                    end_location = len(pdf_content) - 1
                # Search before a keyword
                elif int(rule['location']) == 2:
                    start_location = 0
                    end_location = keyword_location
                # Search entire document
                else:
                    start_location = 0
                    end_location = len(pdf_content) - 1

                string_occurrence = int(rule['string_occurrence'])
                location = int(rule['location'])
                string_formats = rule['string_formats']
                string = ''
                for character in pdf_content[start_location : end_location]: string += character
                if rule['replace_string'] != '' and rule['replace_string'] != None and self.find_match(string_formats, string, location, string_occurrence) != 'NA': self.pdf_data.update({rule['rule_name'] : (rule['csv_column_name'], rule['replace_string'])})
                else: self.pdf_data.update({rule['rule_name'] : (rule['csv_column_name'], self.find_match(string_formats, string, location, string_occurrence))})

        # Reutrn to caller (results stored in object)
        return