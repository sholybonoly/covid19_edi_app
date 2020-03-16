import csv
import configparser

class Team:
    """ Class provides a list of attributes for a given Team """
    name = ''
    email = ''
    postcode = ''

    def __init__(self, name, email, postcode):
        self.name = name
        self.email = email
        self.postcode = postcode
    
    def __str__(self):
        return "Team ( Name: " + self.name + ", Email: " + self.email + ", Postcode: " + self.postcode + ")"

class VolunteerTeams:
    """ Parses CSV File and provides access to a list of Teams """

    csv_file = ''
    teams = {}

    def __str__(self):
        full_string = ''
        for key in self.teams:
            full_string = full_string + str(self.teams[key]) + "\n"
        return full_string


    def __init__(self):
        """ Set up list of teams by reading CSV file (path in config.ini)"""
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.csv_file = config['TEAMS']['CSVFile']

        header_skipped = False
        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue
                team = Team(row[0], row[1], row[2])
                self.teams[row[0]] = team

    def get_all_postcodes(self):
        """ Get all postcodes for all the teams in our config"""
        postcodes = []
        for key in self.teams:
            if (self.teams[key].postcode != ''):
                postcodes.append(self.teams[key].postcode)  
        return postcodes

    def get_email_from_postcode(self, postcode):
        for key in self.teams:
            if(self.teams[key].postcode == postcode):
                print("team [{0}] found from postcode [{1}]".format(self.teams[key].name,postcode))
                return self.teams[key].email
        
        raise Exception("unable to find team for postcode [{0}]".format(postcode))

    def get_group_from_email(self, email):
        for key in self.teams:
            if(self.teams[key].email == email):
                return self.teams[key].name

        raise Exception("unable to find team from email")
        
    def get_all_names(self):
        """ Get the name for all the teams in our config"""
        return list(self.teams.keys())
        
    def get_default_email_address(self):
        """ Get the email address for our default team"""
        return self.teams["Default"].email
