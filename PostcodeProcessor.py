import urllib.request
import json
import math
import configparser
import collections
from collections import namedtuple

class PostcodeProcessor:

    postcode_api = ''

    Location = namedtuple('Location','latitude longitude')
    

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.postcode_api = config.get('POSTCODE','PostcodeApi')

    # user the http://api.postcodes.io API to fetch location data for 
    # postcode
    def getLocationFromPostcode(self,postcode):
        print("fetching location data for [{0}]".format(postcode))
        # take out any whitespace
        postcode = postcode.strip()
        postcode = postcode.replace(" ","")
        reqResult = urllib.request.urlopen(self.postcode_api+postcode).read()
        data = json.loads(reqResult)
        
        latitude = data["result"]["latitude"]
        longitude = data["result"]["longitude"]

        loc = self.Location(latitude,longitude)
        return loc
        # @FIXME: This returns a dictionary of all the relevant data, not just longitude and latitude
        # How do we want it returned? e.g. namedtuple
        
    # this distance function uses the haversine formula 'as the crow flies' (don't ask me to explain the maths!)
    # can read more here: https://www.movable-type.co.uk/scripts/latlong.html
    # it returns a value in meters, rounded up to the nearest whole meter
    def calculateDistance(self,xLat,xLong,yLat,yLong):
        R = 6371e3
        xLatRadians = math.radians(xLat)
        yLatRadians = math.radians(yLat)
        
        latDelta = math.radians(xLat - yLat)
        longDelta = math.radians(xLong - yLong)

        a = math.sin(latDelta/2) * math.sin(latDelta/2) + math.cos(xLatRadians) * math.cos(yLatRadians) * math.sin(longDelta/2) * math.sin(longDelta/2)
            
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = R * c

        return round(d)

    def getDistanceBetweenTwoPostcodes(self,postcodeA, postcodeB):
        locationA = self.getLocationFromPostcode(postcodeA)
        locationB = self.getLocationFromPostcode(postcodeB)

        latitudeA = locationA.latitude
        longitudeA = locationA.longitude
        
        latitudeB = locationB.latitude
        longitudeB = locationB.longitude

        ##print("Postcode [{0}], lat [{1}] long [{2}]".format(postcodeA,latitudeA,longitudeA))
        ##print("Postcode [{0}], lat [{1}] long [{2}]".format(postcodeB,latitudeB,longitudeB))

        distanceInMeters = self.calculateDistance(latitudeA,longitudeA,latitudeB,longitudeB)

        ##print("Distance between [{0}] & [{1}] is [{2}] meters, as the crow flies".format(postcodeA,postcodeB,distanceInMeters))

        return distanceInMeters

    def getNearestNeighbourToPostcode(self, postcode, neighbours):

        print("Finding nearest postcode to [{0}] from [{1}] neighbours".format(postcode,len(neighbours)))

        nearestDistance = self.getDistanceBetweenTwoPostcodes(postcode, neighbours[0])
        nearestPostcode = neighbours[0]
        for neighbour in neighbours:
            distanceToNeighbour = self.getDistanceBetweenTwoPostcodes(postcode, neighbour)
            if(distanceToNeighbour < nearestDistance):
                nearestDistance = distanceToNeighbour
                nearestPostcode = neighbour
            

        print("At [{0}] meters, postcode [{1}] is nearest to postcode [{2}]".format(nearestDistance, nearestPostcode, postcode))
        return nearestPostcode
        


if __name__ == "__main__":
    # Only run this part from the command line
    # Add arguments / options?

    processor = PostcodeProcessor()
    processor.getDistanceBetweenTwoPostcodes("EH87JW","EH68BR")
    print("finding nearest neighbor to EH87JW from the list EH68BR EH395AJ and G1 1RU")
    neighbours = ["EH68BR","EH395AJ","G1 1RU"]
    processor.getNearestNeighbourToPostcode("EH87JW",neighbours)
    #expected output
    #fetching location data for [EH87JW]
    #fetching location data for [EH68BR]
    #Postcode [EH87JW], lat [55.949637] long [-3.148989]
    #Postcode [EH68BR], lat [55.968351] long [-3.166463]
    #Distance between [EH87JW] & [EH68BR] is [2348] meters, as the crow flies