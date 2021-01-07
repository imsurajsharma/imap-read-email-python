from itertools import chain
from email import message_from_bytes
import imaplib, re


imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
imap_ssl_port = 993

username = 'enter_email_address'
password = 'enter your password'


criteria = {
    'FROM': 'Enter_mail_from_name(not add email address)',
    'SUBJECT': 'Enter_Subject_Name',
}

uid_max = 0


def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
    return '(%s)' % ' '.join(chain(*c))


def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()


server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login(username, password)
server.select('INBOX')

result, data = server.uid('search', None, search_string(uid_max, criteria))

uids = [int(s) for s in data[0].split()]
if uids:
    uid_max = max(uids)


server.logout()


while 1:

    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('INBOX')
    result, data = server.uid('search', None, search_string(uid_max, criteria))

    uids = [int(s) for s in data[0].split()]
    for uid in uids:

        if uid > uid_max:
            result, data = server.uid('fetch', str(uid), '(RFC822)')

            msg = message_from_bytes(data[0][1])

            html = msg.get_payload(decode=True).decode('utf-8')

            print(html)

            uid_max = uid


