import imaplib
import smtplib
import email
import re
from email import policy
from datetime import datetime
import configparser
import PostcodeFinder

import smtplib

class EmailRelayProcessor:

    email_address = None
    email_pass = None
    imap_host = None
    imap_port = None
    smtp_host = None
    smtp_port = None
    post_code_processor = None
   
    def __init__(self):
        """ On construction we will get our email settings for reading 
            and forwarding requests as they come in """
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.email_address = config['EMAIL']['Email']
        self.email_pass = config['EMAIL']['Password']
        self.imap_host = config['EMAIL']['IMAPHost']
        self.imap_port = config['EMAIL']['IMAPPort']
        self.smtp_host = config['EMAIL']['SMTPHost']
        self.smtp_port = config['EMAIL']['SMTPPort']
        self.postcode_finder = PostcodeFinder.PostcodeFinder()

    def run(self):
        """ process new messages coming in from to our inbox. """
        M = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
        M.login(self.email_address, self.email_pass)
        M.select('inbox')

        # pick up only emails that have not yet been processed
        (typ, nmsg) = M.search(None, 'NOT (X-GM-LABELS "Processed")')
        if typ != 'OK':
            raise RuntimeError(nmsg)

        for num in nmsg[0].split():
            typ, data = M.fetch(num, '(RFC822)')  
            msg = email.message_from_bytes(data[0][1], policy=policy.default)
            if msg: 

                # got ahead and process the email
                self.processEmail(msg)

                # we mark our email as processed after we successfully
                # complete processing if it drops out at all here we will
                # try again on next run

                #get the UID for this email from mailbox
                (response, data) = M.fetch(num, "(UID)")
                #decode string and extract UID
                uid_string = data[0].decode('utf-8')
                msg_uid = self.parse_uid(uid_string)

                # Mark our email as processed so we don't pick it up again next time
                # This is actually adds a label in google mail
                response = M.uid('COPY', msg_uid, 'Processed')
                if response[0] != 'OK':
                    raise RuntimeError(response[1])

                # this will apply copy changes
                M.expunge()
        
        M.close()
        M.logout()

    def parse_uid(self, uid_string):
        p = re.compile("\d+ \(UID (\d+)\)")
        match = p.match(uid_string)
        return match.group(1)

    def getDateSent(self, msg):
        # determine date that message was originally sent
        date_str = msg.get('date')
        if date_str:
            date_tuple=email.utils.parsedate_tz(date_str)
            if date_tuple:
                return datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))

    def getPlainText(self, msg):
        for part in msg.walk():
            # each part is a either non-multipart, or another multipart message
            # that contains further parts... Message is organized like a tree
            if part.get_content_type() == 'text/plain':
                return part.get_payload() # return the raw text


    def processEmail(self, msg):

        # extract plain text date and subject from email
        text = self.getPlainText(msg)
        subject = msg.get('subject')

        # postcodes 
        postcodes = []
        # first look in the body of the text and if we didn't find anything
        # look in the subject
        postcodes += self.postcode_finder.find_postcodes(text)
        if (len(postcodes) == 0):
            postcodes += self.postcode_finder.find_postcodes(subject)

        # TODO: Not yet fully implemented
        # We get get the postcodes but we this is not yet wired into
        # determine which email it should go to
        # just print out for now
        print("-------------------------------------------------------------------------")
        print(text)
        print("--------")
        print("Found postcodes = " + str(postcodes))

        # TODO: once we figure out which email address to send it to we can use this fowardEmail
        # e.g. self.fowardEmail(msg, 'covid19edapptest1@gmail.com')


    def fowardEmail(self, message, to_addr):

        # just replace the TO as we are sending off to new volunteer team inbox
        # otherwise we are going to forward on the original email as is so we don't
        # miss with the way it was displayed from original sending
        message.replace_header("To", to_addr)

        # open authenticated SMTP connection and send message with
        # specified envelope from and to addresses
        smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
        smtp.starttls()
        smtp.login(self.email_address, self.email_pass)
        smtp.sendmail(self.email_address, to_addr, message.as_string())
        smtp.quit()
     



