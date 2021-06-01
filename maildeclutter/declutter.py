import os
import sys

import maildeclutter.config as CONFIG
import maildeclutter.mailif as mailif


HELPTEXT = """
Mail delcutterer

Access a mailbox over IMAP
"""

def process_actions(mail):
    if len(sys.argv) > 2:
        action = sys.argv[1]

        if action == "view":
            msg = mail.get_mail_message(sys.argv[2])
            print("{}\n\n{}".format(
                msg.headers.get("Subject"),
                msg.get_body()
                ))

        elif action == "headers":
            msg = mail.get_mail_message(sys.argv[2])
            {print(f"{k}: {v}") for k,v in msg.headers.items()}

        elif action == "full":
            msg = mail.get_mail_message(sys.argv[2])
            {print(f"{k}: {v}") for k,v in msg.headers.items()}
            print("")
            print(msg.get_body())

        elif action == "trash":
            mail.trash(sys.argv[2:])

        elif action == "subject":
            message_ids = mail.select('(SUBJECT "{}")'.format(sys.argv[2]))
            print(message_ids)

        elif action == "filter":
            pass
            # Here we want to do a filter that searches on subject content, or body content
            #  through IMAP

        elif action == "rawquery":
            message_ids = mail.select(sys.argv[2])
            print(message_ids)

        else:
            print("Unknown command")


    elif len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "unread":
            print(mail.get_unread_message_ids())

    else:
        print(HELPTEXT)



def main():
    config = CONFIG.load_config()

    mail_options = {
        "imap_server": config["/server/imap"],
        "username": config["/credentials/username"],
        "password": config["/credentials/password"],
        "mailbox": config.get("/server/mailbox", "INBOX"),
    }
    mail = mailif.open(**mail_options)

    try:
        process_actions(mail)

    except BrokenPipeError:
        # Typically when passing through things like `head`
        pass

    finally:
        mail.close()

