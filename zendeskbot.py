import requests
import pprint

# Enter your Zendesk email:
email = '{redacted}'

# Enter your Zendesk token:
token = '{redacted}'

# Enter the view you are connecting to:
view = '{redacted}'

# Build out the zendesk api connection with user creds and ask zendesk for view data:
response = requests.get('https://acquia.zendesk.com/api/v2/views/' + view + '/tickets.json',
                        auth=(email + '/token', token))

# Store data in json in data variable:
data = response.json()

# extracting number of tickets from data:
numberoftickets = data[u'count']

# print the number of tickets in the queue
print('Number of ticket in the queue: %s' % numberoftickets)

print('Ticket IDs in queue:')

# extracting zendesk IDs for tickets (the [0] grabs the first ticket ID, [1] would grab the next and so on)
#ticketids = data[u'tickets'][0][u'id']

# setup a loop to iterate through open tickets and print them
i = 0
while i < numberoftickets:
    print(data[u'tickets'][i][u'id'])
    i += 1

# printing the first open ticket - need to figure out how to iterate through these
#print("The ID of the first open ticket:")
#print(ticketids)

# the below dumps all the data in a readable format
# print("Break")
# pprint.pprint(data)