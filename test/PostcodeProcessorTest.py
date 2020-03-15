#! /usr/bin/python

import os
import unittest 
from collections import namedtuple
from urllib.error import HTTPError
from PostcodeProcessor import PostcodeProcessor

class EmailRelayProcessorTest(unittest.TestCase):
    """ Test class for EmailRelayProcessor
    """

    def setUp(self):
        """  
        
        """
        self.latLongTup=namedtuple("Position","latitude longitude")
        self.postcode1='EH9 3HJ' # Good postcode 1
        self.longLat1=self.latLongTup(55.923219,-3.187863)
        
        self.postcode2='DD4 8QZ' # Non-Edinburgh postcode
        self.postcode3='EH13' # Partial postcode
 
    def test_getLatAndLongFromPostcode1(self):
        """ Test processing of get date sent
        
        """
        
        pstPrc=PostcodeProcessor()
        coords=pstPrc.getLatAndLongFromPostcode(self.postcode1)
        self.assertEqual(coords['result']['latitude'],self.longLat1.latitude)
        self.assertEqual(coords['result']['longitude'],self.longLat1.longitude)
        
    def test_getLatAndLongFromPostcode2(self):
        """ Test processing of get date sent
        
        """
        
        pstPrc=PostcodeProcessor()
        coords=pstPrc.getLatAndLongFromPostcode(self.postcode2)
        self.assertNotEqual(coords['result']['latitude'],self.longLat1.latitude)
        self.assertNotEqual(coords['result']['longitude'],self.longLat1.longitude)
        
    def test_getLatAndLongFromPostcode3(self):
        """ Test processing of get date sent
        
        """
        
        pstPrc=PostcodeProcessor()
        try:
            _coords=pstPrc.getLatAndLongFromPostcode(self.postcode3)
            self.assertTrue(0,'Bad coordinate should not return postcode.')
        except:
            self.assertRaises(HTTPError)
        
        
       
    def test_calculateDistance1(self):
        """
        """
        pass
    
    def test_getDistanceBetweenTwoPostcodes1(self):
        """
        """
        pass
    
    def test_getNearestNeighbourToPostcode1(self):
        """
        """
        pass

#------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
