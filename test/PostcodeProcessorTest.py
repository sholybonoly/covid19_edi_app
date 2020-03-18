#! /usr/bin/python

import os
import math
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
        pstPrc=PostcodeProcessor()
        long1=0.
        lat1=0.
        long2=1.
        lat2=0.
        expDistance = 2*math.pi*6.371e6/360. # 1 degree longitude at equator --> circumference/360
        distance=pstPrc.calculateDistance(lat1, long1, lat2, long2)
        self.assertAlmostEqual(distance, expDistance, delta=20.)
    
    def test_calculateDistance2(self):
        """
        """
        pstPrc=PostcodeProcessor()
        long1=0.
        lat1=1.
        long2=0.
        lat2=0.
        expDistance = 2*math.pi*6.371e6/360. # 1 degree latitude at equator --> circumference/360
        distance=pstPrc.calculateDistance(lat1, long1, lat2, long2)
        self.assertAlmostEqual(distance, expDistance, delta=20.)
    
    def test_calculateDistance3(self):
        """
        """
        pstPrc=PostcodeProcessor()
        long1=0.
        lat1=60.
        long2=1.
        lat2=60.
        expDistance = (math.pi*6.371e6)/360. # 1 degree longitude at 60N --> 0.5* circumference/360
        distance=pstPrc.calculateDistance(lat1, long1, lat2, long2)
        self.assertAlmostEqual(distance, expDistance, delta=20.)
    
    def test_getDistanceBetweenTwoPostcodes1(self):
        """
        """
        pstPrc=PostcodeProcessor()
        postcode1='EH16 6GF'
        postcode2='EH9 3HJ'
        expDistance = 3000.  
        distance=pstPrc.getDistanceBetweenTwoPostcodes(postcode1, postcode2)
        self.assertAlmostEqual(distance, expDistance, delta=100.)
    
    def test_findNearestNNeighboursToPostcode1(self):
        """
        """
        pstPrc=PostcodeProcessor()
        postcode1='EH16 6AA'
        expNeighbours=['EH16 6AJ', 'EH9 3BE', 'EH16 6AD', 'EH16 6AQ', 'EH16 6AH']
        # Finds nearest 5 neighbours within 1 km
        neighbours = pstPrc.findNNearestNeighboursToPostcode(postcode1, 5, 1000)
        self.assertListEqual(neighbours,expNeighbours)

    def test_findNearestNNeighboursToPostcode2(self):
        """
        """
        pstPrc=PostcodeProcessor()
        postcode1='EH16 6AA'
        expNeighbours=['EH16 6AJ', 'EH9 3BE']
        # Finds nearest 5 neighbours within 100m - actually only 2
        neighbours = pstPrc.findNNearestNeighboursToPostcode(postcode1, 5, 100)
        self.assertListEqual(neighbours,expNeighbours)
#------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
