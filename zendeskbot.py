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

# define a global array to store ticket ids
ticketids = []

##################
# api connection #
##################

# Create a function to connect to the Zendesk api, get data and store it in a global variable
def GetResponse():

    # Build out the zendesk api connection with user creds and ask zendesk for view data:
    response = requests.get(url + '/views/' + view + '/tickets.json', auth=(email + '/token', token))

    # grab global variable
    global data

    # Store data in json format in global variable:
    data = response.json()

########################
# Parse and Print loop #
########################

# Create a loop that:
#   - gets data from a global variable
#   - examines data to grab:
#       - number of tickets in the view
#       - ticket numbers
while True:

    # Call the "GetResponse" function to pull data from Zendesk
    GetResponse()

    # extracting number of tickets from data:
    numberoftickets = data[u'count']

    # extracting zendesk IDs for tickets (the [0] grabs the first ticket ID, [1] would grab the next and so on)
    # ticketids = data[u'tickets'][0][u'id']

    # setup a loop to iterate through open tickets and print them when there are tickets to print
    i = 0

    # while i is less than the number of tickets in the view
    while i < numberoftickets:

        # add tickets to ticketids array
        # zendesk IDs for tickets ([0] is the first ticket, [1] would grab the next and so on)
        ticketids.append(data[u'tickets'][i][u'id'])

        # increase value of i by 1
        i += 1

    # print out number of tickers
    print numberoftickets, "tickets"

    # iterate through  ticketids array
    for x in range(len(ticketids)):

        # print each ticket id in the array
        print ticketids[x],

    # empty contents of ticketids array
    print '\n'
    ticketids = []

    # sleep for duration of global poll_interval variable to throttle api access rate
    time.sleep(poll_interval)