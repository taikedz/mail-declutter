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


def get_multipart_sections(message_lines):
    """TODO An email without sections may not have a Content-Type in the main headers

    Main headers with Content-Type specify a "boundary=" key, followed by a hash which may be quoted

    A boundary starts on a new line with "--" followed by the hash, unquoted, and a line end
    A message section part ends with "--", the boundary hash, and a further "--"

    Any section may have a Content-Type containing its own boundary, and so-forth

    This function should return each section that is not of type "multipart/*" (these are container sections) as a Message, but without the boundary
    mail_id should be None

    1. Lookup Content-Type in headers, extract boundary
        --> If none, return None
    2. Continue until first boundary found
    """
    idx = 0
    sections_register = {}

    while idx < len(message_lines):
        line = message_lines[idx]
        if line.startswith("--"):
            m = re.match("Content-Type: (.+?);", message_lines[idx+1])
            if m:
                pass


def get_body(message_lines, headers):
    idx = 0
    while message_lines[idx] != '':
        idx += 1

    #sections = get_multipart_sections(message_lines[idx+1:])

    return os.linesep.join(message_lines[idx+1:])


class Message:
    def __init__(self, message_text, mail_id):
        message_lines = re.split(r"(?:\r\n|\r|\n)", message_text)

        self.headers = parse_headers(message_lines)
        self.body = get_body(message_lines, self.headers)
        self.mail_id = mail_id

    
    def get_body(self):
        return self.body


    def get_headers(self):
        return copy.copy(self.headers)
