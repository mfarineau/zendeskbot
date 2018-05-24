import requests
import pprint
import time

####################
# Define Variables #
####################

# Enter your Zendesk email:
email = '{redacted}'

# Enter your Zendesk token:
token = '{redacted}'

# Enter the view you are connecting to:
view = '{redacted}'

# Enter the Zendesk API url
url = '{redacted}'

# Polling interval (seconds). Zendesk rate limits: https://developer.zendesk.com/rest_api/docs/core/introduction#rate-limits
poll_interval = 10

# define global variable "data" for use in "GetResponse" function
data = 'null'

##################
# api connection #
##################

# Build out the zendesk api connection with user creds and ask zendesk for view data:
def GetResponse():

    response = requests.get(url + '/views/' + view + '/tickets.json',
                            auth=(email + '/token', token))

    # Store data in json format in global data variable:
    global data
    data = response.json()

###################
# Print data loop #
###################

while True:

    # Call the "GetResponse" function to pull data from Zendesk
    GetResponse()

    # extracting number of tickets from data:
    numberoftickets = data[u'count']

    print numberoftickets, "tickets"

    # setup a loop to iterate through open tickets and print them when there are tickets to print
    i = 0
    while i < numberoftickets:
        print(data[u'tickets'][i][u'id'])
        i += 1

    # set a timeout based on global poll_interval
    time.sleep(poll_interval)