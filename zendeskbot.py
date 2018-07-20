#!/usr/bin/env python
import requests
import pprint
import time
import threading
import scrollphathd
from scrollphathd.fonts import font3x5
from credentials import *

scrollphathd.rotate(degrees=180)

####################
# Define Variables #
####################

# Enter your Zendesk email:
email

# Enter your Zendesk token:
token

# Enter the view you are connecting to:
view

# Enter the Zendesk API url
url

# Polling interval (seconds). Zendesk rate limits: https://developer.zendesk.com/rest_api/docs/core/introduction#rate-limits
# Since time.sleep(poll_interval) is used twice, the timeout / sleep time is twice poll_interval.
# So a value of 10 here means the timeout is 20 secondss, which is an api access rate of 3 times per minute.
poll_interval = 10

# define global variable "data" for use in "GetResponse" function
data = 'null'

# define a global array to store ticket ids
ticketids = []

# set a variable to ensure the autoscroll function is only called once
scroll_limit = 0

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
    time.sleep(poll_interval)
    PrintParse()

def autoscroll(interval=0.05):
    threading.Timer(interval, autoscroll, [interval]).start()
    scrollphathd.show()
    scrollphathd.scroll()

########################
# Parse and Print loop #
########################

# Create a loop that:
#   - gets data from a global variable
#   - examines data to grab:
#       - number of tickets in the view
#       - ticket numbers

def PrintParse():

    # Call the "GetResponse" function to pull data from Zendesk
    #GetResponse()

    # extracting number of tickets from data:
    global numberoftickets
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
    print numberoftickets, 'tickets'

    # iterate through  ticketids array
    for x in range(len(ticketids)):

        # print each ticket id in the array
        print ticketids[x],

    # empty contents of ticketids array
    print '\n'
    #ticketids = []
    return numberoftickets
    # sleep for duration of global poll_interval variable to throttle api access rate
    #time.sleep(poll_interval)

# Setup a continuous loop
while True:
    # empty the ticket id array
    ticketids = []

    # Call the Get Reponse function
    GetResponse()

    # Convert ticketids array to string and comma separate values
    ticketids_string = str(ticketids).strip('[]')

    # Convert numberoftickets int to string
    numberoftickets_string = str(numberoftickets)

    # Combine numberoftickets_string and ticketids_string plus text into output variable
    output = '  Tickets: ' + numberoftickets_string + ' IDs: ' + ticketids_string

    # Clear the pi output
    scrollphathd.clear()

    # Watch a queue - if its empty do nothing. If there more than one ticket, output to pi buffer
    if numberoftickets > 0:

        # Write output string to the pi buffer
        scrollphathd.write_string(output, font=font3x5, y=1, brightness=0.5)

    if numberoftickets == 0:

        # Grab the "seconds" component of the current time
        # and convert it to a range from 0.0 to 1.0
        float_sec = (time.time() % 60) / 59.0

        # Multiply our range by 15 to spread the current
        # number of seconds over 15 pixels.
        #
        # 60 is evenly divisible by 15, so that
        # each fully lit pixel represents 4 seconds.
        #
        # For example this is 28 seconds:
        # [x][x][x][x][x][x][x][ ][ ][ ][ ][ ][ ][ ][ ]
        #  ^ - 0 seconds                59 seconds - ^
        seconds_progress = float_sec * 15

        if DISPLAY_BAR:
            # Step through 15 pixels to draw the seconds bar
            for y in range(15):
                # For each pixel, we figure out its brightness by
                # seeing how much of "seconds_progress" is left to draw
                # If it's greater than 1 (full brightness) then we just display 1.
                current_pixel = min(seconds_progress, 1)

                # Multiply the pixel brightness (0.0 to 1.0) by our global brightness value
                scrollphathd.set_pixel(y + 1, 6, current_pixel * BRIGHTNESS)

                # Subtract 1 now we've drawn that pixel
                seconds_progress -= 1

                # If we reach or pass 0, there are no more pixels left to draw
                if seconds_progress <= 0:
                    break

    # Call the autoscroll function that will send the pi buffer to the led screen, but make sure it only runs once
    while scroll_limit < 1:
        autoscroll()
        scroll_limit += 1

    # Sleep for duration of poll_interval to rate limit api access
    time.sleep(poll_interval)