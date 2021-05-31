import os
import sys

import maildeclutter.config as CONFIG
import maildeclutter.mailif as mailif


def main():
    config = CONFIG.load_config()

    mail_options = {
        "imap_server": config["/server/imap"],
        "username": config["/credentials/username"],
        "password": config["/credentials/password"],
        "mailbox": config.get("/server/mailbox", "INBOX"),
    }
    mail = mailif.open(**mail_options)

    if len(sys.argv) > 2:
        mail.fetch(bytes(sys.argv[1], encoding='utf-8'), sys.argv[2])

    else:
        mail.view('UNSEEN')



