import imaplib
import smtplib
import email
import re
from email import policy
from datetime import datetime
import configparser
import PostcodeFinder
import PostcodeProcessor
import VolunteerTeamsConfig
import os
import logging
import requests
import os
from os import path

class EmailRelayProcessor:

    email_address = None
    email_pass = None
    imap_host = None
    imap_port = None
    smtp_host = None
    smtp_port = None
    post_code_processor = None
    volunteer_teams = None
    mailgun_api_key = None
    mailgun_post_url = None
   
    def __init__(self):
        """ On construction we will get our email settings for reading 
            and forwarding requests as they come in """
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.email_address = config['EMAIL']['Email']
        self.email_pass = config['EMAIL']['Password']
        self.imap_host = config['EMAIL']['IMAPHost']
        self.imap_port = config['EMAIL']['IMAPPort']
        self.mailgun_api_key = config['EMAIL']['MailGunAPIKey']
        self.mailgun_post_url = config['EMAIL']['MAINGunPostURL']
        self.postcode_finder = PostcodeFinder.PostcodeFinder()
        self.post_code_processor = PostcodeProcessor.PostcodeProcessor()
        self.volunteer_teams = VolunteerTeamsConfig.VolunteerTeams()

    def run(self):
        """ process new messages coming in from to our inbox. """

        logging.info("Processing inbox " + self.email_address)
        logging.debug("IMAP port " + self.imap_host)
        logging.debug("IMAP port " + self.imap_port)

        try:
            M = imaplib.IMAP4_SSL(self.imap_host)
            M.login(self.email_address, self.email_pass)
            M.select('inbox')
        except Exception as e:
            logging.error(e)


        # pick up only emails that have not yet been processed
        (typ, nmsg) = M.search(None, '(UNSEEN)')
        if typ != 'OK':
            logging.error("Failed to search inbox for non processed emails - " + nmsg)
            raise RuntimeError(nmsg)

        email_nums = nmsg[0].split()

        logging.info(str(len(email_nums)) + " emails to process")

        for num in email_nums:
            typ, data = M.fetch(num, '(RFC822)')  
            msg = email.message_from_bytes(data[0][1], policy=policy.default)
            if msg: 

                # got ahead and process the email
                logging.debug("Processing email - " + num.decode('utf-8'))

                try:
                    self.processEmail(msg)
                except Exception as e:
                    logging.error("Failed to process email. Don't mark it as seen so we can attempt to process again")
                    logging.error(e)
                    # Mark the item as unseen as we didn't successfully process this item
                    M.store(num,'-FLAGS','\Seen')
                    M.expunge()
                    continue
                
                # we mark our email as processed after we successfully
                # complete processing if it drops out at all here we will
                # try again on next run

                #get the UID for this email from mailbox
                (response, data) = M.fetch(num, "(UID)")
                #decode string and extract UID
                uid_string = data[0].decode('utf-8')
                msg_uid = self.parse_uid(uid_string)

                # Mark the item as seen
                M.store(num,'+FLAGS','\Seen')

                # this will apply store changes
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
        logging.debug("Found postcodes in body - " + str(postcodes))
        if (len(postcodes) == 0):
            postcodes += self.postcode_finder.find_postcodes(subject)
            logging.debug("Found postcodes in subject - " + str(postcodes))

        # if we've got some postcodes, determine nearest group and forward email
        if(len(postcodes) != 0):
            # try and find the nearest neighbour, if we have any problems, we forward onto to the default list 
            forwardingEmail = None
            try:
                nearestNeighbour = self.post_code_processor.getNearestNeighbourToPostcode(postcodes[0],self.volunteer_teams.get_all_postcodes())
                logging.debug("nearest neighbour to [{0}] is [{1}]".format(postcodes[0],nearestNeighbour))
                forwardingEmail = self.volunteer_teams.get_email_from_postcode(nearestNeighbour)
                logging.debug("team found (" + forwardingEmail + ")")
            except:
                logging.info("team not found, forwarding to default address")
                forwardingEmail = self.volunteer_teams.get_default_email_address()
        else:
            logging.info("No postcode found in email, forwarding to default address")
            forwardingEmail = self.volunteer_teams.get_default_email_address()

        logging.info("Forwarding email to " + forwardingEmail)
        self.fowardEmail(msg, forwardingEmail)

    def fowardEmail(self, message, to_addr):

        # just replace the TO as we are sending off to new volunteer team inbox
        # otherwise we are going to forward on the original email as is so we don't
        # miss with the way it was displayed from original sending
        message.replace_header("To", to_addr)

        #create a mailgun friendly message based on message object
        response = None
        try:

            #get the message as MIME format so we can pass on intact
            files = {'message': message.as_string()}

            # send email on by using mailgun service
            response = requests.post(
                self.mailgun_post_url,
                auth=("api", self.mailgun_api_key),
                files=files,
                data={"to": to_addr})

            logging.debug("response from mailgun:")
            logging.debug(response.json())

        except Exception as e:
            logging.error("Exception thrown when sending message")
            logging.error(e)

            # rethrow execption so we can catch again
            raise e

        if not response or response.status_code != 200:
            raise Exception("Bad response from request to forward email to mailgun - " + str(response.status_code))

        logging.debug("email sucessfully sent")
     



