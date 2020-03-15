import urllib.request
import json
import math
import configparser

class PostcodeProcessor:

    postcode_api = 'http://api.postcodes.io/postcodes/'

    def init(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        #self.postcode_api = config.get('DEFAULT','PostcodeApi')
        print (self.postcode_api)

    # user the http://api.postcodes.io API to fetch location data for 
    # postcode
    def getLatAndLongFromPostcode(self,postcode):
        print("fetching location data for [{0}]".format(postcode))
        reqResult = urllib.request.urlopen(self.postcode_api+postcode).read()
        data = json.loads(reqResult)
        return data
    
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
        latLongOfA = self.getLatAndLongFromPostcode(postcodeA)
        latLongOfB = self.getLatAndLongFromPostcode(postcodeB)

        latitudeA = latLongOfA["result"]["latitude"]
        longitudeA = latLongOfA["result"]["longitude"]
        
        latitudeB = latLongOfB["result"]["latitude"]
        longitudeB = latLongOfB["result"]["longitude"] 

        print("Postcode [{0}], lat [{1}] long [{2}]".format(postcodeA,latitudeA,longitudeA))
        print("Postcode [{0}], lat [{1}] long [{2}]".format(postcodeB,latitudeB,longitudeB))

        distanceInMeters = self.calculateDistance(latitudeA,longitudeA,latitudeB,longitudeB)

        print("Distance between [{0}] & [{1}] is [{2}] meters, as the crow flies".format(postcodeA,postcodeB,distanceInMeters))

        return distanceInMeters


processor = PostcodeProcessor()
processor.init()
processor.getDistanceBetweenTwoPostcodes("EH87JW","EH68BR")
#expected output
#fetching location data for [EH87JW]
#fetching location data for [EH68BR]
#Postcode [EH87JW], lat [55.949637] long [-3.148989]
#Postcode [EH68BR], lat [55.968351] long [-3.166463]
#Distance between [EH87JW] & [EH68BR] is [2348] meters, as the crow flies