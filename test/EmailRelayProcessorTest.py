#! /usr/bin/python

import os
import unittest 

from email.message import EmailMessage
from datetime import datetime
from EmailRelayProcessor import EmailRelayProcessor

class EmailRelayProcessorTest(unittest.TestCase):
    """ Test class for EmailRelayProcessor
    """

    def setUp(self):
        """ Set up database(s), and other aspects of data selection..
        
        Get a few example email messages  
        
        Set up from auxdir... 
        """
        self.auxDir = os.path.join(os.getenv('COVID19EDAPP'),'auxdir')
        
        self.msg1 = EmailMessage()
        self.msg2 = EmailMessage()
        self.msg3 = EmailMessage()
        
        self.msg1.set_content(''.join(open(os.path.join(self.auxDir,'testMessage1.txt')).readlines()))
        self.msg2.set_content(''.join(open(os.path.join(self.auxDir,'testMessage2.txt')).readlines()))
        self.msg3.set_content(''.join(open(os.path.join(self.auxDir,'testMessage2.txt')).readlines()))
        self.msg1['date'] = datetime(2010,3,1)
        self.msg2['date'] = datetime(2020,4,1)
        self.msg3['date'] = datetime(2020,3,1,12,3)
        
 
    def test_getDateSent1(self):
        """ Test processing of get date sent
        
        """
        
        
        expDateTime = datetime(2010,3,1)
        
        erp=EmailRelayProcessor()
        dateTime1 = erp.getDateSent(self.msg1) 
        self.assertEqual(dateTime1.year,expDateTime.year)
        self.assertEqual(dateTime1.month,expDateTime.month)
        self.assertEqual(dateTime1.day,expDateTime.day)
        self.assertEqual(dateTime1.hour,expDateTime.hour)
        self.assertEqual(dateTime1.minute,expDateTime.minute)
        self.assertEqual(dateTime1.second,expDateTime.second)
        
    def test_getPlainText1(self):
        """
        """
        #expPlainText = 
        erp=EmailRelayProcessor()
        plainText1 = erp.getPlainText(self.msg1)
        # assert test 
        
    
    def test_processMailText1(self):
        """
        """
        erp=EmailRelayProcessor()
        #subject,text,date = self.msg1.
        
    
    def test_run1(self):
        """
        """
        pass

