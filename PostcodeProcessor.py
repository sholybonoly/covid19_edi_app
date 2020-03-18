import os
import urllib.request
import json
import math
import configparser
import collections
from collections import namedtuple
from fastkml import kml
from operator import itemgetter


class PostcodeProcessor:

    postcode_api = ''

    Location = namedtuple('Location','latitude longitude')
    
    postcodeLocationDict = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.postcode_api = config.get('POSTCODE','PostcodeApi')
        self._createPostcodeDictionaryFromKML()

    def _createPostcodeDictionaryFromKML(self):
        """ Reads in kml file converts data to dictionary on postcode.
        Then we can look up quickly later.
        
        """ 
        edinburghPostcodeKmlFile = os.path.join(os.getenv('COVID19EDAPP'),'auxdir','CityOfEdinburghPostcodes.kml')
        # read it using fastkml
        if not os.path.exists(edinburghPostcodeKmlFile):
            raise ValueError("Expected KML file %s does not exist" % edinburghPostcodeKmlFile)
        with open(edinburghPostcodeKmlFile, 'rt', encoding="utf-8") as myfile:
            doc=myfile.read()
        kmlInst = kml.KML()
        kmlInst.from_string(doc)
        
        # Get top layer features
        featuresLayer1 = list(kmlInst.features())
        # Get next layer - individual postcodes layer
        featuresLayer2 = list(featuresLayer1[0].features())
        # Should be 18948 unique Edinburgh postcodes
        if len(featuresLayer2)!=18948:
            raise ValueError("Expected 18948 postcode entries, but number found is %s" % len(featuresLayer2))
        
        # process into dictionary: dict(postcode,Tuple(longitude,latitude)
        self.postcodeLocationDict=dict([(feature.name.strip(),feature.geometry) 
            for feature in featuresLayer2]) 
        


    # user the http://api.postcodes.io API to fetch location data for 
    # postcode
    def getLocationFromPostcode(self,postcode):
        print("fetching location data for [{0}]".format(postcode))
        # take out any whitespace
        try:
            postcode = postcode.replace(" ","")
            postcode = postcode.upper()
            print ("processing post code " + postcode)
            reqResult = urllib.request.urlopen(self.postcode_api+postcode).read()
            # make sure we have JSON in string format
            reqResult = reqResult.decode('utf-8')  
            data = json.loads(reqResult)
        
            latitude = data["result"]["latitude"]
            longitude = data["result"]["longitude"]

            loc = self.Location(latitude,longitude)
            return loc
        except Exception as e:
            print("encountered error when finding location for [{0}]".format(postcode))
            print(e)
            raise Exception("no location found for [{0}]".format(postcode))
        
    def getLocationFromPostcodeKML(self, postcode):
        """ Get location data from KML file 
        
        
        """
        if not self.postcodeLocationDict:
            raise ValueError("Postcode location dictionary has not been initialised from KML file")
        if postcode not in self.postcodeLocationDict:
            raise KeyError("Postcode %s is not a valid Edinburgh postcode" % postcode)
        coords=self.postcodeLocationDict[postcode.strip()]
        # Reverse coordinates to be consistant with previous function
        return self.Location(coords.y,coords.x)
        
    
    # this distance function uses the haversine formula 'as the crow flies' (don't 
    # ask me to explain the maths!). It comes from the main Spherical Trigonometry Equations
    # can read more here: https://www.movable-type.co.uk/scripts/latlong.html
    # it returns a value in meters, rounded up to the nearest whole meter
    def calculateDistance(self,xLat,xLong,yLat,yLong):
        """ Takes lat, long for 2 points 
        
        returns distance in m
        """
        R = 6.371e6 # Mean Earth radius in m
        xLatRadians = math.radians(xLat)
        yLatRadians = math.radians(yLat)
        
        latDelta = math.radians(xLat - yLat)
        longDelta = math.radians(xLong - yLong)

        a = (math.sin(latDelta/2) * math.sin(latDelta/2) + math.cos(xLatRadians) * 
             math.cos(yLatRadians) * math.sin(longDelta/2) * math.sin(longDelta/2))
            
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = R * c

        return round(d)

    def getDistanceBetweenTwoPostcodes(self,postcodeA, postcodeB,useKML=False, isVerbose=False):
        if not useKML:
            locationA = self.getLocationFromPostcode(postcodeA)
            locationB = self.getLocationFromPostcode(postcodeB)
        else:
            locationA = self.getLocationFromPostcodeKML(postcodeA)
            locationB = self.getLocationFromPostcodeKML(postcodeB)
        latitudeA = locationA.latitude
        longitudeA = locationA.longitude
        
        latitudeB = locationB.latitude
        longitudeB = locationB.longitude
        if isVerbose:
            print("Postcode [{0}], lat [{1}] long [{2}]".format(postcodeA,latitudeA,longitudeA))
            print("Postcode [{0}], lat [{1}] long [{2}]".format(postcodeB,latitudeB,longitudeB))

        distanceInMeters = self.calculateDistance(latitudeA,longitudeA,latitudeB,longitudeB)

        ##print("Distance between [{0}] & [{1}] is [{2}] meters, as the crow flies".format(postcodeA,postcodeB,distanceInMeters))

        return distanceInMeters

    def getNearestNeighbourToPostcode(self, postcode, neighbours):
        """ Finds nearest neighbour to postcode.
        
        
        """
        
        print("Finding nearest postcode to [{0}] from [{1}] neighbours".format(postcode,
            len(neighbours)))

        nearestDistance = self.getDistanceBetweenTwoPostcodes(postcode, neighbours[0])
        nearestPostcode = neighbours[0]
        for neighbour in neighbours:
            distanceToNeighbour = self.getDistanceBetweenTwoPostcodes(postcode, neighbour)
            if(distanceToNeighbour < nearestDistance):
                nearestDistance = distanceToNeighbour
                nearestPostcode = neighbour
            

        print("At [{0}] meters, postcode [{1}] is nearest to postcode [{2}]".format(nearestDistance, 
                nearestPostcode, postcode))
        return nearestPostcode
        
    def findNNearestNeighboursToPostcode(self, postcode,numberNeighbours,maxDist=None):
        """ Finds N nearest neighbours within distance (m).
        """
        if numberNeighbours>len(self.postcodeLocationDict):
            print("Number of neighbours requested (%s) is greater than "
                  "number of possible neighbours. Returning %s instead" % (
                      numberNeighbours,len(self.postcodeLocationDict)))
            numberNeighbours=len(self.postcodeLocationDict)    
        if postcode not in self.postcodeLocationDict.keys():
            raise KeyError("%s is an invalid postcode" % postcode)
        distanceList=sorted([(pcode,self.getDistanceBetweenTwoPostcodes(postcode, pcode,useKML=True)) 
             for pcode in self.postcodeLocationDict.keys() if pcode!=postcode],
            key=itemgetter(1))
        print("MD: ",maxDist,len(distanceList))
        if maxDist:
            distanceList=[(pc,dist) for pc,dist in distanceList if dist<maxDist]
        print("MD2: ",len(distanceList))
        numberNeighbours = min(len(distanceList),numberNeighbours)
        return [pc for pc,_dist in distanceList][:numberNeighbours]
        
if __name__ == "__main__":
    # Only run this part from the command line
    # Add arguments / options?

    processor = PostcodeProcessor()
    processor.getDistanceBetweenTwoPostcodes("EH87JW","EH68BR")
    print("finding nearest neighbor to EH87JW from the list EH68BR EH395AJ and G1 1RU")
    neighbours = ["EH68BR","CC","G1 1RU"]
    try:
        processor.getNearestNeighbourToPostcode("EH87JW",neighbours)
    except:
        print("Failed on neighbours")
        
    #expected output
    #fetching location data for [EH87JW]
    #fetching location data for [EH68BR]
    #Postcode [EH87JW], lat [55.949637] long [-3.148989]
    #Postcode [EH68BR], lat [55.968351] long [-3.166463]
    #Distance between [EH87JW] & [EH68BR] is [2348] meters, as the crow flies
    neighbours = processor.findNNearestNeighboursToPostcode("EH16 5AA", 5,100)
    print("Nearest %s neighbours to EH16 5AA within %sm are %s" % (5,100,','.join(neighbours)))
    