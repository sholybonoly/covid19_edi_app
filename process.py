# This is the main runner 
# Run this script to process the next batch of emails
# This could be run in a cron job to periodically check email box

import EmailRelayProcessor

if __name__ == "__main__":
    processor = EmailRelayProcessor.EmailRelayProcessor()
    processor.run()
