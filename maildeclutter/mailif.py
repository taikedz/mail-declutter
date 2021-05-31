import imaplib

def open(imap_server, username, password, mailbox):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select(mailbox)
    
    #help(mail)

    return Gmail(mail)


class Gmail:
    def __init__(self, mail_handle):
        self.mail_handle = mail_handle


    def select(self, flag_str):
        res, message_ids = self.mail_handle.search(None, flag_str)
        return message_ids[0].split()


    def fetch(self, mail_id, message_parts):
        res, data = self.mail_handle.fetch(mail_id, message_parts=message_parts)
        #( status, [parts()])
        print(str(data[0][1], encoding='utf-8'))


    def view(self, search_criteria, peek_mode=False):
        # BODY -- the whole mail
        # BODY[TEXT] --  just the text
        # BODY[HEADER] -- just the headers
        # BODY.PEEK -- same, but do not trigger "\Seen" flag
        view_mode = '(UID BODY[TEXT])'
        if peek_mode:
            view_mode = '(BODY.PEEK[])'

        message_ids = self.select(search_criteria)
        res, data = self.mail_handle.fetch(b'3', message_parts=view_mode)
        #( status, [parts()])
        print(str(data[0][1], encoding='utf-8'))


    def delete(self, flag):
        message_ids = self.select(flag)

        print(message_ids)

        for mid in message_ids:
            pass #result, message = mail.store(mid, '+X-GM-LABELS', '\\Trash')
