import imaplib
import email
import re
from email import policy
from datetime import datetime
import configparser
import PostcodeFinder

class EmailRelayProcessor:

    email_user = ''
    email_pass = ''
    post_code_processor = None
   
    def __init__(self):
        """ On construction we will get email and password for our inbox where requests come in """
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.email_user = config['EMAIL']['Email']
        self.email_pass = config['EMAIL']['Password']
        self.postcode_finder = PostcodeFinder.PostcodeFinder()

    def run(self):
        """ process new messages coming in from to our inbox. """
        M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        M.login(self.email_user, self.email_pass)
        M.select('inbox')

        # pick up only emails that have not yet been processed
        (typ, nmsg) = M.search(None, 'NOT (X-GM-LABELS "Processed")')
        if typ != 'OK':
            raise RuntimeError(nmsg)

        # get list of message IDs (These are not the UIDs just yet)
        msg_ids = nmsg[0].split()

        for num in nmsg[0].split():
            typ, data = M.fetch(num, '(RFC822)')  
            msg = email.message_from_bytes(data[0][1], policy=policy.default)
            if msg: 

                #extract plain text date and subject from email
                text = self.getPlainText(msg)
                date = self.getDateSent(msg)
                subject = msg.get('subject')

                # got ahead and process the email
                self.processMailText(subject, text, date)

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


    def processMailText(self, subject, text, date):

        # postcodes 
        postcodes = []
        # first look in the body of the text and if we didn't find anything
        # look in the subject
        postcodes += self.postcode_finder.find_postcodes(text)
        if (len(postcodes) == 0):
            postcodes += self.postcode_finder.find_postcodes(subject)

        # TODO: Not yet fully implemented
        #  not yet using postcodes - just print them out for now
        print("-------------------------------------------------------------------------")
        print(subject, " - ", date)
        print("--------")
        print(text)
        print("--------")
        print("Found postcodes = " + str(postcodes))


