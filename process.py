# This is the main runner 
# Run this script to process the next batch of emails
# This could be run in a cron job to periodically check email box

import EmailRelayProcessor
import time

if __name__ == "__main__":
    processor = EmailRelayProcessor.EmailRelayProcessor()
    while True:
        print ("Process any incoming emails")
        processor.run()
        print ("Nothing left to process - sleep for 2 seconds")
        time.sleep(2)
    
