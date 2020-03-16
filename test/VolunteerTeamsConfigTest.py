#! /usr/bin/python

import os
import unittest 
from VolunteerTeamsConfig import VolunteerTeams

class VolunteerTeamsConfigTest(unittest.TestCase):
    """ Test class for EmailRelayProcessor
    """

    def setUp(self):
        """  
        
        """
        self.auxDir = os.path.join(os.getenv('COVID19EDAPP'),'auxdir')
        
        
       
        
    def test_get_all_postcodes1(self):
        """ Basic test of get_all_postcodes using default team.csv data 
        """
        vt=VolunteerTeams()
        postcodeList=vt.get_all_postcodes()
        self.assertEqual(len(postcodeList),2,'Number of postcodes = %s, but should equal 2' % len(postcodeList))
    
    def test_get_email_from_postcode1(self):
        """ Test get email from postcode using default data in team.csv
        """
        expEmailAddress = 'covid19edapptest1@gmail.com'
        vt=VolunteerTeams()
        postcodeList=vt.get_all_postcodes()
        
        email=vt.get_email_from_postcode(postcodeList[0])
        self.assertEqual(email,expEmailAddress,'email = %s, but should equal %s' % (email,expEmailAddress))
    
    
    def test_get_group_from_email1(self):
        """ test get group from email address for default case
        """
        expGroupName = 'Test Team 1'
        vt=VolunteerTeams()
        emailAddress = 'covid19edapptest1@gmail.com' 
        
        groupName=vt.get_group_from_email(emailAddress)
        self.assertEqual(groupName,expGroupName,'group = %s, but should equal %s' % (
            groupName,expGroupName))
    
    
    def test_get_all_names1(self):
        """ Test get all names for default case
        """
        vt=VolunteerTeams()
        allNamesList = vt.get_all_names()
        self.assertEqual(len(allNamesList),3,'N(names) = %s, expected 3' % len(allNamesList))
        allUniqueNames = list(set(allNamesList))
        self.assertEqual(len(allUniqueNames),3,'N(unique names) = %s, expected 3' % len(allUniqueNames))
        
        
    def test_get_default_email_address1(self):
        """ Test get default email
        """
        expDefEmailAddress = 'covid19edapptest3@gmail.com'
        vt=VolunteerTeams()
        defaultEmailAddress = vt.get_default_email_address()
        self.assertEqual(defaultEmailAddress,expDefEmailAddress,"Default email address = %s, expected = %s" 
                         % (defaultEmailAddress,expDefEmailAddress))
        
        
    
    

#------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
