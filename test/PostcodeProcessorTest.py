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
 
    def test_getLocationFromPostcode1(self):
        """ Test processing of location from postcode
        
        """
        
        pstPrc=PostcodeProcessor()
        coords=pstPrc.getLocationFromPostcode(self.postcode1)
        self.assertEqual(coords.latitude,self.longLat1.latitude)
        self.assertEqual(coords.longitude,self.longLat1.longitude)
        
    def test_getLoctionFromPostcode2(self):
        """ Test processing of location from postcode
        
        """
        
        pstPrc=PostcodeProcessor()
        coords=pstPrc.getLocationFromPostcode(self.postcode2)
        self.assertNotEqual(coords.latitude,self.longLat1.latitude)
        self.assertNotEqual(coords.longitude,self.longLat1.longitude)
        
    def test_getLocationFromPostcode3(self):
        """ Test processing of get date sent
        
        """
        
        pstPrc=PostcodeProcessor()
        try:
            _coords=pstPrc.getLocationFromPostcode(self.postcode3)
            self.assertTrue(0,'Bad coordinate should not return postcode.')
        except:
            self.assertRaises(HTTPError)
        
    def test_getLocationFromPostcodeKML1(self):
        """ Test processing of location from postcode
        
        """
        
        pstPrc=PostcodeProcessor()
        coords=pstPrc.getLocationFromPostcodeKML(self.postcode1)
        self.assertEqual(coords.latitude,self.longLat1.latitude)
        self.assertEqual(coords.longitude,self.longLat1.longitude)
        
    def test_getLocationFromPostcodeKML2(self):
        """ Test processing of location from postcode
        Outside Edinburgh / invalid 
        
        """
        
        pstPrc=PostcodeProcessor()
        try:
            _coords=pstPrc.getLocationFromPostcodeKML(self.postcode2)
            self.assertTrue(0,'Bad coordinate should not return postcode.')
        except:
            self.assertRaises(KeyError)    
        
    def test_getLocationFromPostcodeKML3(self):
        """ Test processing of get date sent
        
        """
        
        pstPrc=PostcodeProcessor()
        try:
            _coords=pstPrc.getLocationFromPostcodeKML(self.postcode3)
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
