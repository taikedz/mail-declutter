import re
import os
import copy


def parse_headers(message_lines):
    remade_line = []
    headers = {}
    idx = 0
    while message_lines[idx] != '':
        remade_line.append(message_lines[idx])

        if (message_lines[idx+1] == '' or not re.match(r"\s", message_lines[idx+1][0])):
            full_line = "".join(remade_line)
            m = re.match("^(.+?): (.*)$", full_line)
            headers[m.group(1)] = m.group(2)
            
            remade_line = []

        idx += 1

    return headers


def get_body(message_lines):
    idx = 0
    while message_lines[idx] != '':
        idx += 1

    return os.linesep.join(message_lines[idx+1:])


class Message:
    def __init__(self, message_text, mail_id):
        message_lines = re.split(r"(?:\r\n|\r|\n)", message_text)

        self.headers = parse_headers(message_lines)
        self.body = get_body(message_lines)
        self.mail_id = mail_id

    
    def get_body(self):
        return self.body


    def get_headers(self):
        return copy.copy(self.headers)
