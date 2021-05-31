import imaplib

from maildeclutter.message import Message

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


    def get_mail_message(self, mail_id):
        # BODY -- the whole mail
        # BODY[TEXT] --  just the text
        # BODY[HEADER] -- just the headers
        # BODY.PEEK -- same, but do not trigger "\Seen" flag
        view_mode = '(BODY.PEEK[])'

        res, data = self.mail_handle.fetch(bytes(mail_id, encoding='utf-8'), message_parts='(BODY.PEEK[])')
        return Message(str(data[0][1], encoding='utf-8'), mail_id)


    def get_unread_message_ids(self):
        message_ids = self.select("UNSEEN")
        return message_ids


    def trash(self, message_ids):
        for mid in message_ids:
            result, message = mail.store(mid, '+X-GM-LABELS', '\\Trash')
