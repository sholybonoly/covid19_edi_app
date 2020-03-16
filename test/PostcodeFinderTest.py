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
        self.msg1 = self.read_test_file(os.path.join(self.auxDir,'testMessage1.txt'))
        self.postcodeList1=['EH165AA']

        # Partial postcode.
        self.msg2 = self.read_test_file(os.path.join(self.auxDir,'testMessage2.txt'))
        self.postcodeList2 = []

        # Outside Edinburgh 
        self.msg3 = self.read_test_file(os.path.join(self.auxDir,'testMessage3.txt'))
        self.postcodeList3 = []

        # Mixed up in text 
        self.msg4 = self.read_test_file(os.path.join(self.auxDir,'testMessage4.txt'))
        self.postcodeList4 = ['EH93HJ']

        # List 
        self.msg5 = self.read_test_file(os.path.join(self.auxDir,'testMessage5.txt'))
        self.postcodeList5 = ['EH93HJ','EH32BD', 'EH43HG', 'EH139DH', 'EH166DF']

        # EHno in other context
        self.msg6 = self.read_test_file(os.path.join(self.auxDir,'testMessage6.txt'))
        self.postcodeList6 = []

        # Lower case postcode
        self.msg7 = self.read_test_file(os.path.join(self.auxDir,'testMessage7.txt'))
        self.postcodeList7 = ['EH165AA']


    def read_test_file(self, filepath):
        f = open(filepath)
        lines = ''.join(f.readlines())
        f.close()
        return lines
        
        
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
    

    def test_find_postcodes7(self):
        """ Test to see if it handles lower case ok
        
        """
    
        pstFdr=PostcodeFinder()
        postcodeList=pstFdr.find_postcodes(self.msg7)
        self.assertListEqual(postcodeList,self.postcodeList7,
            'Post code list %s does not match expected list  %s: message = %s' % (
                postcodeList,self.postcodeList6,self.msg6))      
   

#------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
