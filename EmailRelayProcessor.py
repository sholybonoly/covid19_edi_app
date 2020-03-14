import imaplib
import email
from email import policy
from datetime import datetime
import configparser

class EmailRelayProcessor:

    email_user = ''
    email_pass = ''
    last_processed = ''
   
    def init(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.email_user = config['DEFAULT']['Email']
        self.email_pass = config['DEFAULT']['Password']
        self.last_processed = datetime.strptime(config['DEFAULT']['ProcessFrom'], '%Y-%m-%d %H:%M:%S')
        print (self.last_processed)


    def run(self):
        # process new messages coming in from to our inbox.
        M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        M.login(self.email_user, self.email_pass)
        M.select('inbox')

        print ("Processing emails since ", self.last_processed)

        since = self.last_processed.strftime('%d-%b-%Y')
        since_str = "(SINCE \"" + since + "\")"; 

        #TODO the SINCE string is not working yet
        # so its just processing all emails right now
        (typ, nmsg) = M.search(None, 'ALL')

        for num in nmsg[0].split():
            typ, data = M.fetch(num, '(RFC822)')  
            msg = email.message_from_bytes(data[0][1], policy=policy.default)
            text = self.getPlainText(msg)
            date = self.getDateSent(msg)
            subject = msg.get('subject')
            self.processMailText(subject, text, date)

        M.close()
        M.logout()


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
        #not yet implemented just print out messages
        print("-------------------------------------------------------------------------")
        print(subject, " - ", date)
        print("--------")
        print(text)



#Process the latest emails in our inbox
processor = EmailRelayProcessor()
processor.init()
processor.run()
