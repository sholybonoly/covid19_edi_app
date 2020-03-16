import re
import configparser

class PostcodeFinder:

    prefix = 'EH'

    def __init__(self):
        # get the prefix we are using for postcodes from our config file
        # e.g. we only look for Edinburgh postcodes
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.prefix = config.get('POSTCODE','Prefix')        

    def find_postcodes(self, text):
        """ Find any postcodes in the text provided """
        
        # First look for any full postcodes
        # We will use these first
        # Ignore case and we don't care if there is a space between beginning and end

        matches = re.findall(self.prefix + '\d+\s*\d\w\w', text, re.IGNORECASE)

        # Our PostcodeProcessor does not support partial poscodes yet
        # We could extend this look for partial postcodes at later point in time.
        #if len(matches) == 0:
            # If didn't find any whole postcodes 
            # Look for partial postcode (just prefix and digit)
            #matches = re.findall(r"\b" + self.prefix + '\d+' +r"\b", text, re.IGNORECASE)

        # get red of any spaces in postcode so they all match each other
        # make it uppercase so they are all the same
        postcodes = []
        for match in matches:
            postcode = match.replace(" ", "")
            postcode = postcode.replace("\n", "")
            postcode = postcode.upper()
            postcodes.append(postcode)

        # return all the postcodes we found
        return postcodes


        
   