#! /usr/bin/python

import os
import unittest 
from PostcodeFinder import PostcodeFinder

class PostcodeFinderTest(unittest.TestCase):
    """ Test class for EmailRelayProcessor
    """

    def setUp(self):
        """  
        
        """
        self.auxDir = os.path.join(os.getenv('COVID19EDAPP'),'auxdir')
        
        
        # Good postcode
        self.msg1=''.join(open(os.path.join(self.auxDir,'testMessage1.txt')).readlines())
        self.postcodeList1=['EH165AA']
        # Partial postcode.
        self.msg2=''.join(open(os.path.join(self.auxDir,'testMessage2.txt')).readlines())
        self.postcodeList2 = []
        # Outside Edinburgh 
        self.msg3=''.join(open(os.path.join(self.auxDir,'testMessage3.txt')).readlines())
        self.postcodeList3 = []
        # Mixed up in text 
        self.msg4=''.join(open(os.path.join(self.auxDir,'testMessage4.txt')).readlines())
        self.postcodeList4 = ['EH93HJ']
        # List 
        self.msg5=''.join(open(os.path.join(self.auxDir,'testMessage5.txt')).readlines())
        self.postcodeList5 = ['EH93HJ','EH32BD', 'EH43HG', 'EH139DH', 'EH166DF']
        # EHno in other context
        self.msg6=''.join(open(os.path.join(self.auxDir,'testMessage6.txt')).readlines())
        self.postcodeList6 = []
        
        
    def test_find_postcodes1(self):
        """ Test to see if it picks up postcodes from text correctly
        
        """
    
        
        pstFdr=PostcodeFinder()
        postcodeList=pstFdr.find_postcodes(self.msg1)
        self.assertListEqual(postcodeList,self.postcodeList1,
            'Post code list %s does not match expected list  %s: message = %s' % (
                postcodeList,self.postcodeList1,self.msg1))
        
    def test_find_postcodes2(self):
        """ Test to see if it picks up postcodes from text correctly
        
        """
    
        
        pstFdr=PostcodeFinder()
        postcodeList=pstFdr.find_postcodes(self.msg2)
        self.assertListEqual(postcodeList,self.postcodeList2,
            'Post code list %s does not match expected list  %s: message = %s' % (
                postcodeList,self.postcodeList1,self.msg2))
    
    def test_find_postcodes3(self):
        """ Test to see if it picks up postcodes from text correctly
        
        """
    
        
        pstFdr=PostcodeFinder()
        postcodeList=pstFdr.find_postcodes(self.msg3)
        self.assertListEqual(postcodeList,self.postcodeList3,
            'Post code list %s does not match expected list  %s: message = %s' % (
                postcodeList,self.postcodeList3,self.msg3))
        
    def test_find_postcodes4(self):
        """ Test to see if it picks up postcodes from text correctly
        
        """
    
        
        pstFdr=PostcodeFinder()
        postcodeList=pstFdr.find_postcodes(self.msg4)
        self.assertListEqual(postcodeList,self.postcodeList4,
            'Post code list %s does not match expected list  %s: message = %s' % (
                postcodeList,self.postcodeList4,self.msg4))
    
    def test_find_postcodes5(self):
        """ Test to see if it picks up postcodes from text correctly
        
        """
    
        
        pstFdr=PostcodeFinder()
        postcodeList=pstFdr.find_postcodes(self.msg5)
        self.assertListEqual(postcodeList,self.postcodeList5,
            'Post code list %s does not match expected list  %s: message = %s' % (
                postcodeList,self.postcodeList5,self.msg5))
        
    def test_find_postcodes6(self):
        """ Test to see if it picks up postcodes from text correctly
        
        """
    
        
        pstFdr=PostcodeFinder()
        postcodeList=pstFdr.find_postcodes(self.msg6)
        self.assertListEqual(postcodeList,self.postcodeList6,
            'Post code list %s does not match expected list  %s: message = %s' % (
                postcodeList,self.postcodeList6,self.msg6))
    
          
   

#------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
