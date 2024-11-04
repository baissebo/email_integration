import email
import imaplib
from email.header import decode_header
from email.utils import parsedate_to_datetime

from django.utils import timezone

from email_app.models import EmailMessage


def fetch_messages(account, password):
    username = account.email

    if "gmail.com" in username:
        imap_server = "imap.gmail.com"
    elif "yandex.ru" in username:
        imap_server = "imap.yandex.ru"
    elif "mail.ru" in username:
        imap_server = "imap.mail.ru"
    else:
        raise ValueError("Неподдерживаемый почтовый оператор")

    try:
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(username, password)
    except imaplib.IMAP4.error as ime:
        raise ValueError(f"Ошибка при подключении к IMAP серверу: {str(ime)}")

    imap.select("inbox")
    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()

    fetched_messages = []

    for email_id in email_ids:
        res, msg = imap.fetch(email_id, "(RFC822)")
        for response_part in msg:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode() if isinstance(subject, bytes) else subject
                date_sent = parsedate_to_datetime(msg["Date"])
                date_received = timezone.now()
                body = ""
                attachments = []

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode("utf-8")
                        elif part.get("Content-Disposition") is not None:
                            filename = part.get_filename()
                            if filename:
                                attachments.append(filename)

                else:
                    body = msg.get_payload(decode=True).decode("utf-8")

                EmailMessage.objects.create(
                    account=account,
                    subject=subject,
                    date_sent=date_sent,
                    body=body,
                    attachments=attachments
                )

                fetched_messages.append({
                    "subject": subject,
                    "date_sent": date_sent,
                    "body": body,
                    "attachments": attachments
                })

    imap.close()
    imap.logout()

    return fetched_messages
