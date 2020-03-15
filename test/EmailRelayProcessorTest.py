#! /usr/bin/python

import unittest 
from email.message import EmailMessage
from email.headerregistry import Address
from EmailRelayProcessor import EmailRelayProcessor

class EmailRelayProcessorTest(unittest.TestCase):
    """ Test class for EmailRelayProcessor
    """

    def setUp(self):
        """ Set up database(s), and other aspects of data selection..
        
        Get a few example email messages  
        
        Set up from auxdir... 
        """
        self.auxDir = 
        
        self.msg1 = EmailMessage()
        self.msg2 = EmailMessage()
        self.msg3 = EmailMessage()
        
        self.msg1.set_content(open(os.path.join(self.auxDir,'testMessage1.txt').readlines()))
        self.msg2.set_content(open(os.path.join(self.auxDir,'testMessage2.txt').readlines()))
        self.msg3.set_content(open(os.path.join(self.auxDir,'testMessage2.txt').readlines()))
        self.msg1['Date'] = 
 
    def test_getDateSent1():
        """ Test processing of get date sent
        
        """
        
        
        expDateTime = 
        
        erp=EmailRelayProcessor()
        dateTime1 = erp.getDateSent(self.msg1) 
        self.assertTrue(dateTime1.year,expDateTime.year)
        self.assertTrue(dateTime1.month,expDateTime.month)
        self.assertTrue(dateTime1.day,expDateTime.day)
        self.assertTrue(dateTime1.hour,expDateTime.hour)
        self.assertTrue(dateTime1.minute,expDateTime.minute)
        self.assertTrue(dateTime1.second,expDateTime.second)
        
    def test_getPlainText1(self):
        """
        """
        expPlainText = 
        erp=EmailRelayProcessor()
        plainText1 = erp.getPlainText(self.msg1)
        # assert test 
        
    
    def test_processMailText1(self):
        """
        """
        erp=EmailRelayProcessor()
        subject,text,date = self.msg1.
        
    
    def test_run1(self):
        """
        """
        pass

